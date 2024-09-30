import pandas as pd
import re

terms_df = pd.read_csv("/data/economic_terms.csv", encoding='utf-8-sig')

def load_news():
   with open("data/news.txt", "r", encoding="utf-8") as file:
    news_content = file.read()
    
    return news_content 


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

