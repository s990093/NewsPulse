import pandas as pd

from src.gpt import analyze_with_gpt
import threading
from rich.progress import Progress
from rich.console import Console
import concurrent.futures
import re
from concurrent.futures import ThreadPoolExecutor, as_completed



console = Console()

def load_data(file_path):
    """Load CSV data."""
    return pd.read_csv(file_path)


def get_filtered_data(file_path, id_gourp):
    df = load_data(file_path)  # 加載數據
    filtered_df = df[df['類別'] == id_gourp][['ID']]  # 篩選類別 id 為 4，並選取所需的列
    return filtered_df


def get_summary_report(file_path, filtered_df):
    # 加載 respt.csv
    respt_df = pd.read_csv(file_path)  # 假設respt.csv中有ID和summary_report列
    # 使用ID進行數據合併
    # 使用filtered_df的ID與respt_df的news_id進行數據合併
    merged_df = pd.merge(filtered_df, respt_df[['news_id', 'summary_report']], left_on='ID', right_on='news_id', how='left')
    # 刪除news_id列，因為它和ID已經對應
    merged_df.drop(columns=['news_id'], inplace=True)    
    
    return merged_df



def split_and_summarize(text, task_prompt, max_tokens):
    """
    對超過最大 token 限制的文本進行拆分並總結
    :param text: 要處理的文本
    :param task_prompt: 用於指導總結的提示字串
    :param max_tokens: GPT 回應的最大 token 數
    :return: 最終摘要
    """
    
    # 將 task_prompt 更新以引導總結
    task_prompt += f"幫我獲取關鍵內容，{task_prompt}"
    sub_summaries = []
    sentences = re.split(r'(?<=[.!?]) +', text)  # 根據句子結尾符號分割

    current_chunk = ""
    futures = []

    # 使用 ThreadPoolExecutor 來處理分析
    with ThreadPoolExecutor(max_workers=15) as executor:
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_tokens // 2:
                current_chunk += sentence + " "
            else:
                future = executor.submit(analyze_with_gpt, current_chunk.strip(), task_prompt, max_tokens=1500)
                futures.append(future)
                current_chunk = sentence + " "  # 開始新的 chunk

        # 處理最後一個 chunk
        if current_chunk:
            future = executor.submit(analyze_with_gpt, current_chunk.strip(), task_prompt, max_tokens=1500)
            futures.append(future)

        for future in as_completed(futures):
            summary = future.result()
            sub_summaries.append(summary)

    # 確保最終摘要不超過 max_tokens
    final_summary = " ".join(sub_summaries)
    
    # 如果摘要超過 max_tokens，則遞規總結
    while len(final_summary.split()) > max_tokens:
        final_summary = split_and_summarize(final_summary, task_prompt, max_tokens)
        
    # last summary and final summary < max_tokens
    final_summary = analyze_with_gpt(final_summary, task_prompt, max_tokens=2000, temperature=0.2)


    return final_summary

def process_batch(batch, task_prompt, max_tokens=1500, max_workers=20, *args, **kwargs):
    """
    將一個批次的新聞列表進行處理並合成成一篇摘要文章
    :param batch: 新聞列表 (新聞文本的列表)
    :param task_prompt: 用於指導總結的提示字串
    :param max_tokens: GPT 回應的最大 token 數
    :param max_workers: 最大同時執行的線程數
    :return: 該批次的合成文章
    """
    
    
    # 將該批次的新聞轉換成一個長文本
    batch_text = " ".join(batch)
    
    # 如果文本的 token 超過限制，就分段處理
    if len(batch_text) > max_tokens:
        task_prompt += f"目前內文太長幫我使用最短內容，{task_prompt}"

        sub_summaries = []
        
        # 使用正則表達式查找完整的句子
        sentences = re.split(r'(?<=[.!?]) +', batch_text)  # 根據句子結尾符號分割
        
        current_chunk = ""
        futures = []  # 存儲 futures

        # 使用 ThreadPoolExecutor 並設置最大線程數
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_tokens // 2:
                    current_chunk += sentence + " "
                else:
                    # 提交當前的 chunk 處理
                    future = executor.submit(analyze_with_gpt, current_chunk.strip(), task_prompt, max_tokens=2000, temperature=0.2)
                    futures.append(future)
                    current_chunk = sentence + " "  # 開始新的 chunk
            
            # 處理最後一個 chunk
            if current_chunk:
                future = executor.submit(analyze_with_gpt, current_chunk.strip(), task_prompt, max_tokens=2000, temperature=0.2)
                futures.append(future)

            # 收集所有的摘要
            for future in as_completed(futures):
                summary = future.result()
                sub_summaries.append(summary)

        combined_summary = " ".join(sub_summaries)
        
        
        if len(combined_summary) > max_tokens:
            final_summary =  split_and_summarize(combined_summary, task_prompt, 1000)
            # print(final_summary)
        else:
            final_summary = analyze_with_gpt(combined_summary, task_prompt, max_tokens=2000, temperature=0.2)
    else:
        # 如果文本長度在限制內，直接總結
        final_summary = analyze_with_gpt(batch_text, task_prompt, max_tokens=2000, temperature=0.2)
        
        
        
    return final_summary



def _summarize_news_in_batches(news_list, initial_task_prompt, final_task_prompt, batch_size=5, pool_size=3, *args, **kwargs):
    # Step 1: Initial summaries (assuming they are already summarized)
    initial_summaries = news_list
    

    # Step 2: Summarize each batch separately
    new_summaries = []  # 儲存每次批次合成後的文章

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]正在處理批次總結...", total=(len(initial_summaries) // batch_size) + 1)

        # 使用 ThreadPoolExecutor 來控制 pool 大小
        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            futures = []
            for i in range(0, len(initial_summaries), batch_size):
                batch = initial_summaries[i:i + batch_size]

                # 每個批次合成成一篇文章
                future = executor.submit(process_batch, batch, initial_task_prompt)
                futures.append(future)

                # 更新進度條
                progress.update(task, advance=1)

            # 收集每次批次處理後的結果
            for future in concurrent.futures.as_completed(futures):
                result = future.result()  # 每個批次的合成文章
                new_summaries.append(result)  # 保存合成後的文章
                
    
    # Step 3: 最後對每個批次合成的結果進行進一步總結，使用 final_task_prompt
    final_summary = process_batch(new_summaries, final_task_prompt)

    # Return the final comprehensive summary
    return final_summary



def summarize_news_in_batches(news_list, batch_size=5, pool_size=3):
    # 初始總結的提示，強調統計和趨勢識別
    initial_task_prompt = (
        "以下是幾篇新聞的簡要摘要，請總結這些新聞。"
        "同時進行數據統計，找出新聞中反覆提及的主題、趨勢、人物和事件，並指出其相關性。"
        "請保留與這些主題和趨勢一致的新聞。"
    )

    # 最終總結的提示，要求詳細報告並強調統計數據，說明大部分新聞的共同點
    final_task_prompt = (
        "請撰寫一篇詳細且連貫的文章，總結這些新聞，專注於最重要的主題和討論。"
        "請特別指出大部分新聞都提及的主題、趨勢或關鍵人物，並總結這些資訊。"
        "可以列出新聞中最常出現的主題、人物、趨勢和關鍵事件。"
    )
    
    # 傳入統計分析提示
    return _summarize_news_in_batches(news_list, initial_task_prompt, final_task_prompt, batch_size, pool_size)


def summarize_topic_news(news_list, batch_size=2, pool_size=3):
    # 第一階段的任務提示
    initial_task_prompt = """
    針對台灣市場，以下是幾篇新聞文章的分類總結，請對每篇文章進行摘要，並僅保留與主題一致的新聞：
    1. 請對新聞做出簡短的總結，包含文章的關鍵要點、重要細節和對台灣的影響。
    2. 僅保留與主題一致的文章，刪除任何不相關的資訊或內容。
    3. 確保每篇摘要能夠獨立存在，易於理解並能夠反映原文的核心思想，適合通勤者在短時間內獲取信息。
    """

    # 第二階段的任務提示：最終統整
    final_task_prompt = """
    現在請撰寫一篇詳細且連貫的文章來總結這些新聞，聚焦於最重要的主題，並闡述次要但值得關注的內容：
    1. 根據前面整理出的新聞摘要，統整出主要主題，明確指出這些主題的重要性和對台灣的影響。
    2. 詳細說明與該主題密切相關的重要討論，提供支持數據或具體例證以增強說服力。
    3. 補充次要但值得關注的報導內容，說明其相關性和潛在影響，並建議未來可能的發展方向。
    4. 在結尾處，提供對於未來的預測或行動建議，使讀者能夠對該主題有更深入的理解。
    """
    
    # 調用內部函數進行批量總結
    return _summarize_news_in_batches(news_list, initial_task_prompt, final_task_prompt, batch_size, pool_size)
