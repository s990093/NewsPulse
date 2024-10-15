import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# 1. 加载 CSV 文件
file_path = 'data/analysis_report.csv'  
df = pd.read_csv(file_path)

# 2. 确保所有文本为字符串
df['extracted_news_info'] = df['extracted_news_info'].astype(str)  # 确保所有文本为字符串

# 3. 加载预训练的 tokenizer 和模型
tokenizer = AutoTokenizer.from_pretrained("hw2942/bert-base-chinese-finetuning-financial-news-sentiment-v2")
model = AutoModelForSequenceClassification.from_pretrained("hw2942/bert-base-chinese-finetuning-financial-news-sentiment-v2")

# 4. 定义获取 BERT 嵌入向量的函数
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():  # 禁用梯度计算以节省内存
        outputs = model(**inputs)
    return outputs.logits.numpy()  # 获取模型输出的 logits

# 5. 获取所有有效文本的嵌入向量
valid_texts = df['extracted_news_info'].dropna().tolist()  # 确保有效输入
embeddings = np.array([get_embedding(text) for text in valid_texts])  # 获取嵌入

embeddings = embeddings.reshape(len(valid_texts), -1)  # Reshape to (num_samples, num_features)

scaler = StandardScaler()
embeddings = scaler.fit_transform(embeddings)

# 检查嵌入的维度
print("Shape of embeddings:", embeddings.shape)

# 6. 聚类嵌入向量
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters)
df['cluster'] = kmeans.fit_predict(embeddings)  # 直接在 DataFrame 中添加聚类标签
print("Shape of embeddings after reshaping and normalization:", embeddings.shape)

# 7. 降维到二维
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

# 8. 可视化聚类结果
plt.figure(figsize=(12, 8))
sns.scatterplot(x=reduced_embeddings[:, 0], y=reduced_embeddings[:, 1], hue=df['cluster'], palette='Set1', s=100)

# 添加每个点的文本标签
for i, txt in enumerate(valid_texts):  # 使用有效文本
    plt.annotate(i + 1, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]), fontsize=9, alpha=0.7)

plt.title('BERT Embeddings Clustering Visualization')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()
