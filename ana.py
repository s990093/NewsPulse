import csv
from src.gpt import generate_content_to_markdown
from src.extraction import *

from rich.console import Console
from rich.text import Text

console = Console()
if __name__ == "__main__":
    
    # file_path = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/classify_news.csv'
    # respt_file = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/report.csv'

    # # 多個主題
    # topics = [0,1,2,3,4]  # 假設主題為 4, 5, 6，你可以根據需要修改

    # all_final_summaries = []

    # for topic in topics:
    #     # 針對每個主題提取 filtered_data
    #     filtered_data = get_filtered_data(file_path, topic)
        
    #     # 生成報告
        # final_result = get_summary_report(respt_file, filtered_data)

    #     news_list = final_result["summary_report"].tolist()
    #     print(f"主題 {topic} 的新聞數量 -> {len(news_list)}")

    #     # 假設你有多篇新聞文本存儲在 news_list 中
    #     final_summary = summarize_news_in_batches(news_list, 5,8)

    #     # 將每個主題的結果以 (主題, 總結) 的形式添加到列表中
    #     all_final_summaries.append([topic, final_summary])

    #  # 將所有主題的總結保存到 CSV 文件，保留換行符
    # with open('/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/final_summary.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     # 寫入 CSV 標題
    #     writer.writerow(["Topic", "Summary"])

    #     # 寫入每個主題的總結，保留 \n
    #     for summary in all_final_summaries:
    #         writer.writerow([summary[0], summary[1]])
            
            
    # print("Summaries saved to final_summary.csv")


    # CSV 文件路徑
    csv_file = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/final_summary.csv'

    # 讀取 CSV 並顯示文章
    # with open(csv_file, newline='', encoding='utf-8') as csvfile:
    df = load_data(csv_file)
    
    data = df["Summary"].tolist()
    final_summary = summarize_topic_news(data)

    res = generate_content_to_markdown(final_summary, 4000)
    
    print(res)
    
    


         