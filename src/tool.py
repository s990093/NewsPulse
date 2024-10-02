import pandas as pd
import re
import spacy
import jieba
import logging
import csv

jieba.setLogLevel(logging.WARNING)

# terms_df = pd.read_csv("data/economic_terms.csv", encoding='utf-8-sig')
# 讀取正面詞彙
with open('data/positive_words.txt', 'r', encoding='big5') as f:
    positive_words = f.read().splitlines()

# 讀取負面詞彙
with open('data/negative_words.txt', 'r', encoding='big5') as f:
    negative_words = f.read().splitlines()



def check_economic_terms(news_content):

    # 將經濟單詞轉換為列表
    economic_terms = terms_df['經濟單詞'].tolist()
    
    # 將經濟單詞轉換為正則表達式模式
    pattern = r'\b(' + '|'.join(map(re.escape, economic_terms)) + r')\b'
    
    # 使用 re.search 檢查是否有匹配的經濟單詞
    if re.search(pattern, news_content):
        return True  # 含有經濟單詞
    else:
      return False  # 不含有經濟單詞

def analyze_sentiment_ratio(text):
    # 使用 jieba 斷詞
    words = jieba.cut(text)

    # 計算正面和負面詞彙的數量
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    # 計算情感分數比例
    total_count = positive_count + negative_count
    if total_count == 0:
        return 0  # 若沒有情感詞彙，返回0分

    sentiment_ratio = (positive_count - negative_count) / total_count

    return sentiment_ratio



def extract_economic_entities(text):
    """
    從輸入的新聞文本中提取經濟相關的命名實體（如金錢、日期、百分比、組織等）

    :param text: str, 新聞內容
    :return: list of tuples, 提取的經濟實體和對應的標籤
    """
    # 使用 NLP 模型進行文本處理
    nlp = spacy.load("zh_core_web_trf")

    doc = nlp(text)

    # 提取經濟相關的命名實體
    economic_entities = []
    for ent in doc.ents:
        # 只提取經濟相關的實體
        if ent.label_ in ["MONEY", "DATE", "PERCENT", "ORG"]:  # 可根據需要擴展標籤
            economic_entities.append((ent.text, ent.label_))

    return economic_entities


def sanitize_input(value):
    """清理輸入的字符串，去除不必要的換行符號和空格。"""
    return  str(value).replace('\n', ' ').replace('\r', ' ').strip()
    

def export_to_csv(id, title, sentiment_result, sentiment_ratio, trend_result, extracted_news_info, summary_report, compression_ratio, country, filename='data/analysis_report.csv'):
    # 清理輸入數據
    id = id
    sentiment_result = sanitize_input(sentiment_result)
    trend_result = sanitize_input(trend_result)
    summary_report = sanitize_input(summary_report)

    # 使用 'a' 模式打開檔案以便於追加
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 如果是新檔案，寫入標題行
        if file.tell() == 0:  # 檔案是空的，寫入標題行
            writer.writerow(['ID', 
                             'title',
                             'extracted_news_info',
                             'summary_report',
                             'sentiment_result',
                             'trend_result',
                             'sentiment_ratio',
                             'compression_ratio',
                             'country'])
        
        # 寫入分析結果
        writer.writerow([id,
                         title,
                         extracted_news_info,
                         summary_report,
                         sentiment_result,
                         trend_result, 
                         sentiment_ratio,
                         compression_ratio,
                         country])
        
        
