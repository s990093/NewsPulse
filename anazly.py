import numpy as np
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# 1. 加載 CSV 文件
file_path = 'data/analysis_report.csv'  
df = pd.read_csv(file_path)

# 中文分词函数
def preprocess_text(text):
    words = text.split('/')  # 使用分隔符分割文本
    return ' '.join(words)  # 返回以空格连接的词语

# 對 'extracted_news_info' 列進行中文分詞

source = "extracted_news_info"
df['extracted_news_info'] = df[source].apply(preprocess_text)

# 2. 載入 BERT 模型和 tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')  # 使用中文 BERT
model = BertModel.from_pretrained('bert-base-chinese')

# 3. 將文本轉換為 BERT 的輸入格式並獲取輸出向量
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():  # 禁用梯度計算以節省內存
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # 獲取 [CLS] token 的輸出向量，並去掉多餘的維度

# 4. 獲取所有文本的嵌入向量
embeddings = [get_embedding(text) for text in df['extracted_news_info']]


# 5. 計算相似度矩陣
# 計算相似度矩陣
similarity_matrix = cosine_similarity(embeddings)

# 僅計算上三角矩陣的相似度
unique_similarities = []

for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        unique_similarities.append((df['ID'][i], df['ID'][j], similarity_matrix[i][j]))

# 6. 輸出相似度矩陣
print("相似度矩陣：")
print(similarity_matrix)

# 設定相似度閾值
threshold = 0.8
for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        if similarity_matrix[i][j] >= threshold:
            print(f"相似的文本: {df['ID'][i]} 與 {df['ID'][j]} 相似度: {similarity_matrix[i][j]}")





# 假設 df 是你的 DataFrame，similarity_matrix 是相似度矩陣
# 這裡使用 df['ID'] 來標記行和列
ids = df['ID'].values

# 設定相似度閾值

# 繪製相似度熱圖
binary_similarity_matrix = np.where(similarity_matrix >= 0.8, 0.7, 0)

plt.figure(figsize=(10, 8))
# 使用 seaborn 的 heatmap 繪製
sns.heatmap(binary_similarity_matrix, 
            annot=False,        # 不顯示數值
            cmap="coolwarm",   # 顏色映射
            xticklabels=ids,   # x 軸標籤
            yticklabels=ids,   # y 軸標籤
            mask=(similarity_matrix < threshold),  # 隱藏低於閾值的值
            cbar_kws={'label': '相似度'})  # 顯示顏色條的標籤

plt.title(source)
plt.xlabel('ID')
plt.ylabel('ID')
plt.show()