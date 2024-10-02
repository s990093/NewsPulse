import re
import pandas as pd
from newspaper import Source
from datetime import datetime

# 设置搜索时间和关键字
search_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
search_key = "示例关键字"  # 替换为实际的搜索关键字

url = "https://money.udn.com/money/index"
# 创建一个新闻源对象
source = Source(url)  # 替换为你想爬取的网站URL


domain = re.findall('https://[^/]*', url)[0].replace('https://', '')
# 下载和构建网页内容
source.build()

# 提取新闻文章
articles = source.articles  # 获取所有文章的列表

# 用于存储提取的数据
rows = []

# 遍历每篇文章并提取信息    
for article in articles:
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

    
    print("content len -> ",len(content))
    
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

# 打印 DataFrame
print(df)

# 保存到 CSV 文件
csv_file_path = 'news_data.csv'  # 你希望保存的文件名
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')  # 保存为 CSV 文件，避免编码问题

print(f"数据已保存到 {csv_file_path}") 