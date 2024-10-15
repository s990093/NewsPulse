import csv
import random
import time
import openai
import pandas as pd

from src.helper import clean_string, detect_language, preprocess_content
# from src.tool import analyze_sentiment_ratio, export_to_csv
from src.ENV import TASKS
from src.news import NewsArticle
import logging
from rich.console import Console

import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from transformers import AutoModelForSequenceClassification,AutoTokenizer,pipeline
import traceback


model = AutoModelForSequenceClassification.from_pretrained('uer/roberta-base-finetuned-chinanews-chinese')
tokenizer = AutoTokenizer.from_pretrained('uer/roberta-base-finetuned-chinanews-chinese')

text_classification = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

console = Console()


api_keys = ["sk-JsX1k5W4cJmkII0F005273A2E4D1430eBf1bB38a92Dc33Fb",
       "sk-ouapzZyTJaNSUAO480744a8693F446B1B1A552Da73A05971",
       "sk-IjlK3saoqmSqp22f3842B88e8fCd44F0AfD2D8E841C9FaF7"
       ]

openai.base_url = "https://free.gpt.ge/v1/"
openai.default_headers = {"x-foo": "true"}


country_max_retries = 5

def extract_country_code(news_id, summary_report, news_content, max_retries=4):
    """
    提取文章的國家代碼，最多重試 max_retries 次。
    如果無法從摘要中提取國家代碼，則切換到新聞內容並修改提示詞進行提取。

    參數:
        news_id (int): 新聞ID，用於打印日誌。
        summary_report (str): 新聞的摘要內容。
        news_content (str): 新聞的完整內容。
        max_retries (int): 最大重試次數，默認為4次。

    返回:
        str: 提取到的國家代碼，若提取失敗則返回空字串。
    """
    
    country_analysis_prompt = "根據文章內容，判斷該文章的主要國家，回傳國家英文大寫簡寫例如US、CN等），簡短直接，移除多餘內容。"
    fallback_prompt = "根據新聞內容，判斷該文章的主要國家,回傳國家英文大寫簡寫例(例如US、CN等），簡短直接，移除多餘內容。"
    
    for attempt in range(max_retries):
            # 第一次使用摘要，之後嘗試使用新聞全文
            if attempt == 0:
                prompt = country_analysis_prompt
                content = summary_report
            else:
                prompt = fallback_prompt
                content = news_content
            
            country = clean_string(analyze_with_gpt(content, prompt))
            
            print(f"嘗試第 {attempt + 1} 次提取國家代碼: {country}")
            
            # 檢查是否成功提取國家代碼，並且符合兩位字母的格式
            if country and len(country) <= 4 and country.isalpha():
                country = country.upper()
                return country  # Successfully extracted a country code, return result
            
            # If extraction fails but the content mentions "台灣" or "Taiwan", return "TW"
            if "台灣" in content or "Taiwan" in content:
                return "TW"

            # Check the detected language to determine if we should attempt extraction
            detected_language = detect_language(content)
            
            if detected_language == "en":
                # If detected language is English, and country code is two letters, return it
                if country and len(country) <= 4 and country.isalpha():
                    return country.upper()  # Return uppercase country code

        
    print(f'新聞ID: {news_id} - 無法提取有效的國家代碼 {country}')

    return None  # 返回 None 表示提取失敗





def analyze_with_gpt(content, task_prompt, model="gpt-3.5-turbo-0125", temperature=0, max_tokens=200, top_p=1, frequency_penalty=0.0, presence_penalty=0.0):
    """
    This function uses the OpenAI GPT model to generate a response based on the given content and task prompt.

    Parameters:
    - content (str): The input text content for the GPT model.
    - task_prompt (str): The task prompt that guides the GPT model's response.
    - model (str): The GPT model to be used. Default is "gpt-3.5-turbo-0125".
    - temperature (float): The randomness of the GPT model's output. Default is 0.
    - max_tokens (int): The maximum number of tokens to generate. Default is 200.
    - top_p (float): The nucleus sampling parameter. Default is 1.
    - frequency_penalty (float): The penalty for repeating the same words. Default is 0.0.
    - presence_penalty (float): The penalty for repeating the same phrases. Default is 0.0.

    Returns:
    - str: The generated response from the GPT model. If an error occurs, returns "Error in generating response".
    """
    
    openai.api_key = random.choice(api_keys)

    try:
        completion = openai.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=[
                {"role": "system", "content": task_prompt},
                {"role": "user", "content": content}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # print("Traceback:")
        # traceback.print_exc()  # 打印錯誤堆棧
        # print( {"role": "system", "content": task_prompt},
        #         {"role": "user", "content": content})
        return "Error in generating response"

def analyze_news(news_id, news_content, news_title, export = True, filename = "report.csv"):
    """
    分析新聞內容的經濟相關性，提取摘要和關鍵資訊。
    
    參數:
        news_id (int): 新聞文章的ID。
        news_content (str): 新聞文章的完整內容。
        news_title (str): 新聞文章的標題。
    
    返回:
        tuple: 包含新聞ID、相關性比率、情感比率和國家代碼的元組。
    """
    
    start_time = time.time()
    
    news_content = preprocess_content(news_content)
    
    # 確認內容長度
    if len(news_content) <= 20:
        print(f'新聞ID: {news_id} - 此新聞內容過短。')
        return None

    # 經濟相關性分析
    relation_prompt = "這篇新聞是否與經濟或股票有關？請回答用情緒回答我要計算。 繁體字"
    is_relation = clean_string(analyze_with_gpt(news_title, relation_prompt))
    relation_ratio = analyze_sentiment_ratio(is_relation)

    # 判斷經濟相關性
    if relation_ratio < 0.08:
        print(f'新聞ID: {news_id} - 此新聞與經濟無關。相關性比率: {relation_ratio}')
        return None

    # 總結新聞內容
    summary_prompt = "提取新聞中的重要資訊，移除無關內容，簡短且直接，100字以內。繁體字"
    summary_report = clean_string(analyze_with_gpt(news_content, summary_prompt))

    # 提取標題
    title_prompt = "根據內容提取簡短且直接的標題，移除無關內容。繁體字"
    title = clean_string(analyze_with_gpt(summary_report, title_prompt))

    # 提取關鍵字
    news_extraction_prompt = ("根據內容提供7個關鍵名詞，"
                               "格式為單行字串用/分隔，"
                               "不得使用其他格式或換行。")
    
    extracted_news_info = ""
    for attempt in range(3):  # 限制最多重試3次
        extracted_news_info = clean_string(analyze_with_gpt(summary_report, news_extraction_prompt))
        if extracted_news_info and "/" in extracted_news_info and "\n" not in extracted_news_info:
            break
        else:
            print(f"第 {attempt + 1} 次重試提取新聞資訊失敗，請重試。")

    if not extracted_news_info:
        print(f'新聞ID: {news_id} - 無法提取有效的新聞資訊。')
        return None
    

    # 計算字數
    original_word_count = len(news_content.split())
    summary_word_count = len(summary_report.split())
    compression_ratio = (original_word_count / summary_word_count) if summary_word_count > 0 else float('inf')

    # 情感分析
    sentiment_prompt = "針對以下新聞內容進行情感分析，簡短直接，移除多餘內容。繁體字"
    sentiment_result = clean_string(analyze_with_gpt(summary_report, sentiment_prompt))
    sentiment_ratio = analyze_sentiment_ratio(sentiment_result)

    # 趨勢分析
    trend_analysis_prompt = "提供簡短的趨勢分析，重點簡述趨勢。繁體字"
    trend_result = clean_string(analyze_with_gpt(sentiment_result, trend_analysis_prompt))

    # 國家代碼提取，最多重試 country_max_retries 次
    country = extract_country_code(news_id, summary_report, news_content)

    elapsed_time = time.time() - start_time

    # 匯出結果到 CSV
    if export:
        export_to_csv(news_id,
                    title,
                    sentiment_result, 
                    sentiment_ratio, 
                    trend_result, 
                    extracted_news_info,
                    summary_report,
                    compression_ratio,
                    country,
                    filename=filename)

    return news_id, relation_ratio, sentiment_ratio, country, elapsed_time


def retry_news(news_content, task_prompt, validation_func, additional_hint, max_retries=5):
    """
    尝试分析新闻内容，直到获得符合要求的结果或超过最大尝试次数。

    :param news_content: 新闻内容
    :param task_prompt: 任务提示
    :param validation_func: 结果验证函数
    :param max_retries: 最大尝试次数
    :return: 符合要求的结果或最后一次结果
    """
    attempts = 0  # 尝试次数
    cleaned_result = None  # 初始化结果

    while attempts < max_retries:
        result = analyze_with_gpt(news_content, task_prompt)  # 调用 GPT 分析
        
        cleaned_result = clean_string(result)  # 清理结果

        # 使用验证函数检查结果
        if validation_func(cleaned_result):
            return cleaned_result  
        
        
        attempts += 1 
        current_prompt = f"{task_prompt} {additional_hint} 已經錯誤 請確保回答滿足格式要求。 {attempts} 次數了。"
        
        
        print(task_prompt)

        if attempts < max_retries:
            print(f"结果不符合限制，将再次尝试 (尝试次数: {attempts})")

    print(f"超过最大尝试次数，使用最后一次结果: {cleaned_result}")
    
    
    return cleaned_result 


def get_sentiment_score(text):
    """
    使用BERT模型分析文本情感，并返回-1, 0, 1的情感分数。
    """
        
    result = text_classification(text)

  
    return result[0]["score"]


def analyze_news_v0(news_id, news_content, news_title, export=True, filename="report.csv"):
    news_content = preprocess_content(news_content)
    
    
    # 確認內容長度
    if len(news_content) <= 20:
        print(f'新聞ID: {news_id} - 此新聞內容過短。')
        return None
    
    
    # 經濟相關性分析
    relation_prompt = "這篇新聞是否與經濟或股票有關？請回答用情緒回答我要計算。 繁體字"
    is_relation = clean_string(analyze_with_gpt(news_title, relation_prompt))
    relation_ratio = analyze_sentiment_ratio(is_relation)

    # 判斷經濟相關性
    if relation_ratio < 0.08:
        print(f'新聞ID: {news_id} - 此新聞與經濟無關。相關性比率: {relation_ratio}')
        return None

   
    # 用於保存結果的列表
    results = []
    results.append(news_id)
    
    # 總結新聞內容
    summary_prompt = "提取新聞中的重要資訊，移除無關內容，簡短且直接，100字以內。繁體字"
    summary_report = clean_string(analyze_with_gpt(news_content, summary_prompt))

    
    # 遍历每个任务并调用 `retry_news`
    for task_name, task_info in TASKS.items():
        task_prompt = task_info["prompt"]
        
        res = ""
        
        if task_name == "FinRE":
            for attempt in range(3):  # 限制最多重試3次
                res = clean_string(analyze_with_gpt(summary_report, task_prompt))
                if res and "/" in res and "\n" not in res:
                    break
                else:
                    print(f"第 {attempt + 1} 次重試提取新聞資訊失敗，請重試。")

            if not res:
                print(f'新聞ID: {news_id} - 無法提取有效的新聞資訊。')
                return None
        elif task_name == "FinNA":
            res = clean_string(analyze_with_gpt(summary_report, task_prompt))
        
        results.append(res)
        

    results.append(summary_report)
    
    
    # 情感分析
    sentiment_prompt = "針對以下新聞內容進行情感分析。繁體字"
    sentiment_result = clean_string(analyze_with_gpt(summary_report, sentiment_prompt))

    results.append(get_sentiment_score(sentiment_result))
    
    # 显示 DataFrame
    
    if export:
        # 打开文件并写入数据
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=',')  # You can change delimiter if needed

            # 如果文件为空，写入表头
            if file.tell() == 0:
                writer.writerow(["news_id", "FinRE", "FinNA", "summary_report", "sentiment_analysis"])  # Adjust headers based on your needs

            # 写入每一行的结果
            writer.writerow(results)  # Write the entire results list as a row
            
            
def generate_content_to_markdown(content: str, max_tokens: int = 200) -> str:
    """
    Converts a given text content into markdown format for better readability.

    Parameters:
    - content (str): The input text content to be converted.
    - max_tokens (int): The maximum number of tokens allowed for the markdown conversion. Default is 200.

    Returns:
    - str: The converted markdown content.
    """
    # 設定 Markdown 提示
    markdown_prompt = (
        f"請將以下文章內容轉換為美觀的Markdown格式，"
        f"保留內容不變，並添加適當的標題、清單和格式。\n\n"
        f"要求：\n"
        f"- 使用主標題（#）為整體文章命名。\n"
        f"- 針對每個段落或主題使用副標題（## 或 ###）。\n"
        f"- 如果有列表或重點，請使用無序或有序列表。\n"
        f"- 使用粗體和斜體來強調重要的詞語或句子。\n"
        f"- 確保格式整齊，便於閱讀和理解。\n\n"
        f"以下是要轉換的內容：\n\n"
    )


    # 調用 analyze_with_gpt 函數，傳遞內容和提示
    markdown_content = analyze_with_gpt(content, markdown_prompt, max_tokens=max_tokens)

    return markdown_content
