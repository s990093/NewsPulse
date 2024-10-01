import numpy as np
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载 CSV 文件
df = pd.read_csv('data/analysis_report.csv')

# 2. 初始化 BERT tokenizer 和 model
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
source = "extracted_news_info"

# 3. 定义获取 BERT 嵌入向量的函数
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# 4. 获取有效文本并提取嵌入向量
valid_texts = df[source].dropna().astype(str).tolist()
embeddings = np.array([get_embedding(text) for text in valid_texts])

# 5. 聚类嵌入向量
num_clusters = 6
kmeans = KMeans(n_clusters=num_clusters)
df['cluster'] = kmeans.fit_predict(embeddings)

# 6. PCA 降维至二维
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

# 7. 可视化聚类结果
plt.figure(figsize=(12, 8))
sns.scatterplot(x=reduced_embeddings[:, 0], y=reduced_embeddings[:, 1], hue=df['cluster'], palette='Set1', s=100)

for i, _ in enumerate(valid_texts):
    plt.annotate(i + 1, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]), fontsize=9, alpha=0.7)

plt.title('BERT Embeddings Clustering Visualization')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()


# from sklearn.metrics import silhouette_score

# best_k = 0
# best_score = -1
# for k in range(2, 11):
#     kmeans = KMeans(n_clusters=k)
#     labels = kmeans.fit_predict(embeddings)
#     score = silhouette_score(embeddings, labels)
#     print(f'k={k}, Silhouette Score={score}')
#     if score > best_score:
#         best_k = k
#         best_score = score

# print(f'最佳聚类数: {best_k}，对应的轮廓系数: {best_score}')