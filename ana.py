# import csv
# from src.gpt import generate_content_to_markdown
from src.extraction import *
# 匯入套件 & 選擇模型
# from langchain_ffm import ChatFormosaFoundationModel
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import threading
# llm = ChatFormosaFoundationModel()
from langchain_openai import OpenAI
from rich.console import Console
# from rich.text import Text

console = Console()

file_path = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/classify_news.csv'
respt_file = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/report.csv'

if __name__ == "__main__":
    
    

    # 多個主題
    topics = [0,1,2,3,4]  # 假設主題為 4, 5, 6，你可以根據需要修改

    all_final_summaries = []
    
    filtered_data = get_filtered_data(file_path, 0)
    final_result = get_summary_report(respt_file, filtered_data)
    # 
    news_list = final_result["summary_report"].tolist()
    

    # for topic in topics:
    #     # 針對每個主題提取 filtered_data
    #     filtered_data = get_filtered_data(file_path, topic)
        
#         # 生成報告
        # final_result = get_summary_report(respt_file, filtered_data)

#         news_list = final_result["summary_report"].tolist()
#         print(f"主題 {topic} 的新聞數量 -> {len(news_list)}")

#         # 假設你有多篇新聞文本存儲在 news_list 中
#         final_summary = summarize_news_in_batches(news_list, 2, 15)

#         # 將每個主題的結果以 (主題, 總結) 的形式添加到列表中
#         all_final_summaries.append([topic, final_summary])

#     # 寫入純文本文件，並在每篇新聞之間加入分隔符
#     with open('/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/final_summary.txt', 'w', encoding='utf-8') as file:
#         # 遍歷所有的總結
#         for index, summary in enumerate(all_final_summaries, start=1):
#             file.write(f"News {index}\n")  # 編號每篇新聞
#             file.write(f"Topic: {summary[0]}\n")  # 寫入主題
#             file.write(f"Summary: {summary[1]}\n")  # 寫入摘要
#             file.write("-" * 40 + "\n")  # 用分隔線區分新聞

            
#     print("Summaries saved")
    
    
#     # 讀取純文本文件並解析每篇新聞
#     with open('/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/final_summary.txt', 'r', encoding='utf-8') as file:
#         content = file.read()  # 讀取整個文件內容

#     # 以分隔符來分割每篇新聞
#     news_sections = content.strip().split("-" * 40)  # 根據分隔線切割

#     # 解析每篇新聞
#     news_list = []
#     for section in news_sections:
#         lines = section.strip().split("\n")  # 按行分割
#         if len(lines) >= 3:  # 確保每篇至少有標題和摘要
#             topic = lines[1].replace("Topic: ", "").strip()  # 提取主題
#             summary = lines[2].replace("Summary: ", "").strip()  # 提取摘要
#             news_list.append({"topic": topic, "summary": summary})  # 將主題和摘要存儲為字典

#     # 示範輸出讀取到的新聞
#     for news in news_list:
#         print(f"Topic: {news['topic']}")
#         print(f"Summary: {news['summary']}\n")


    # # CSV 文件路徑
    # csv_file = '/Users/hungwei/Desktop/Proj/NewsPulse/classify_news/final_summary.csv'

    # # 讀取 CSV 並顯示文章
    # # with open(csv_file, newline='', encoding='utf-8') as csvfile:
    # df = load_data(csv_file)
    
    # data = df["Summary"].tolist()
    # final_summary = summarize_topic_news(data)

    # res = generate_content_to_markdown(final_summary, 4000)
    
    # print(res)
    
    


			

llm = OpenAI(api_key="sk-JsX1k5W4cJmkII0F005273A2E4D1430eBf1bB38a92Dc33Fb")

# llm.openai_api_base = "https://free.gpt.ge/v1/"
# llm.default_headers = {"x-foo": "true"}

# 切割文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = text_splitter.create_documents(news_list)

# map 函數
def map_summary(index, content, results, failed_indices):
	try:
		prompt = PromptTemplate.from_template("請將以下內容進行摘要: {text}")
		chain = prompt | llm
		summary = chain.invoke(content).content
		results[index] = summary
	except Exception as e:
		failed_indices.append(index)
		print(f"Error processing document {index}: {e}")

# 使用 map 函數進行平行運算
def process_documents(documents):
	results = [None] * len(documents)
	failed_indices = []
	threads = []
	
	for i, doc in enumerate(documents):
		t = threading.Thread(target=map_summary, args=(i, doc, results, failed_indices))
		t.start()
		threads.append(t)

	for t in threads:
		t.join()

	return results, failed_indices

# 取得 map 結果並且合併
results, failed_indices = process_documents(documents)
map_result = '\n'.join(results)

# reduce 函數
def reduce_summary(results):
	prompt = PromptTemplate.from_template("請將以下內容進行摘要: {text}")
	chain = prompt | llm
	reduced_summary = chain.invoke(results).content
	return reduced_summary

# 輸出最終結果
results = reduce_summary(map_result)
print(results)