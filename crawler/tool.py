import re
import pandas as pd
from newspaper import Article
from datetime import datetime

def extract_article_data(article_urls, search_key):
    # 设置搜索时间
    search_time = datetime.now().isoformat()  # 当前时间

    # 用于存储提取的数据
    rows = []

    # 遍历每篇文章并提取信息
    for i, url in enumerate(article_urls):
        article = Article(url)  # 创建文章对象
        article.download()  # 下载文章内容
        article.parse()     # 解析文章
        
        # 提取所需的信息
        title = article.title
        link = article.source_url
        pub_date = article.publish_date.isoformat() if article.publish_date else datetime.now().isoformat()
        description = article.summary  # 简介
        news_url = article.source_url  # 新闻链接
        content = article.text  # 文章内容
        content = content.replace('\r', ' ').replace('\n', ' ')
        
    
        print(i, len(content))

        # 获取域名
        domain = re.findall('https://[^/]*', url)[0].replace('https://', '')
        
        # 将数据添加到 rows 列表
        rows.append({
            'search_time': search_time,
            'search_key': search_key,
            'title': title,
            'link': link,
            'pub_date': pub_date,
            'description': description,
            'source': domain,
            'newsUrl': news_url,
            'content': content
        })

    # 创建 DataFrame
    df = pd.DataFrame(data=rows, columns=['search_time', 'search_key', 'title', 'link', 'pub_date', 'description', 'source', 'newsUrl', 'content'])

    return df

# 示例文章 URL 列表
article_urls = [
    'https://money.udn.com/money/story/5599/8252576?from=edn_newestlist_vipbloomberg',  # 替换为实际的文章链接
    
]

