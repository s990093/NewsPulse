import pandas as pd
from src.gpt import analyze_with_gpt

# 读取 JSON 文件
df = pd.read_json("data/clustering_results.json")
cluster_0_data = df[df['Cluster'] == 0]

# 读取 CSV 文件
# file_path = 'data/analysis_report.csv'
# analysis_df = pd.read_csv(file_path)

def recursive_summarization(highlights, threshold=3):
    # 如果 highlights 的長度小於 threshold，則返回它們的摘要
    if len(highlights) < threshold:
        content = "\n".join(highlights)  
        
        task_prompt = "提取給總結，先說比較重要的，可以比較詳細，可以比較口語化，給我純文字"
        # 调用 GPT API 进行分析
        summary = analyze_with_gpt(content, task_prompt, max_tokens=500)
        return summary

    # 取出前 threshold 篇重點
    current_batch = highlights[:threshold]
    remaining_highlights = highlights[threshold:]

    content = "\n".join(current_batch) 
    task_prompt = "找出共通性與給重點，如果沒有共通性就列出比較重要的：\n"
    
    # 调用 GPT API 进行分析
    summary = analyze_with_gpt(content, task_prompt, max_tokens=250)

    # 继续递归处理剩余的重点
    return recursive_summarization(remaining_highlights + [summary], threshold)

def process_cluster():
    # 提取所有 ID
    ids = cluster_0_data['ID'].tolist()  # 获取所有 ID 的列表
    
    # 示例：如果需要在 analysis_df 中进一步处理这些 ID，可以这样做
    filtered_analysis = analysis_df[analysis_df['ID'].isin(ids)]
    
    # 提取 summary_report 列
    highlights = filtered_analysis['summary_report'].tolist()  # 获取 summary_report 列的列表
        
    # 使用递归摘要函数处理提取的亮点
    final_summary = recursive_summarization(highlights)
    
    # 创建一个新的 DataFrame 存储 ID 和摘要
    summary_df = pd.DataFrame({
        'Cluster_ID': 0, 
        'Summary':  [final_summary]
    })
    
    # 将 DataFrame 保存到 CSV 文件
    output_file_path = 'data/cluster_summaries.csv'
    summary_df.to_csv(output_file_path, index=False)

    print(f"Summaries saved to {output_file_path}")