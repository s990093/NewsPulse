import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 讀取合併後的 CSV 檔案
merged_data = pd.read_csv('data.csv')

# 為每篇文章生成唯一的 id，從 1 開始
merged_data['id'] = merged_data.index + 1

# 確保 pub_date 為 datetime 格式，這裡直接使用 pd.to_datetime
merged_data['pub_date'] = pd.to_datetime(merged_data['pub_date'], errors='coerce')

# 計算文章數量
article_count = merged_data.shape[0]
print(f'Total number of articles: {article_count}')

# 計算每個 source 的文章數量
source_counts = merged_data['source'].value_counts()
print("\nNumber of articles by source:")
print(source_counts)

# 查看每個 search_key 的文章數量
search_key_counts = merged_data['search_key'].value_counts()
print("\nNumber of articles by search key:")
print(search_key_counts)

# 計算每天的文章數量
daily_counts = merged_data['pub_date'].dt.date.value_counts().sort_index()

# 計算 content 的長度並加入 DataFrame
merged_data['content_length'] = merged_data['content'].str.len()

# 計算平均 content 長度
average_content_length = merged_data['content_length'].mean()
print(f'\nAverage content length: {average_content_length:.2f} characters')

# 繪製每日文章數量的折線圖
plt.figure(figsize=(12, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')
plt.title('Number of Articles Published Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

# 生成 word cloud
text = ' '.join(merged_data['content'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# 顯示 word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不顯示坐標軸
plt.show()

# 將更新後的 DataFrame 保存回 CSV 檔案
merged_data.to_csv('news_data_updated.csv', index=False)
