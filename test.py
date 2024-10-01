import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

# 读取 CSV 文件
file_path = 'data/analysis_report.csv'  # 替换为你的 CSV 文件路径
df = pd.read_csv(file_path)

# 简化分词函数，直接根据 "/" 进行分割
def preprocess_text(text):
    words = text.split('/')
    return ' '.join(words)

# 应用文本预处理
df['cleaned_summary'] = df['extracted_news_info'].apply(preprocess_text)

# 初始化 TF-IDF 向量化器，限制特征数量并过滤词汇
vectorizer = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.8)

# 将清理后的文本转换为 TF-IDF 向量
tfidf_matrix = vectorizer.fit_transform(df['cleaned_summary'])

# 聚类 - 使用 MiniBatchKMeans 将数据分为 5 个簇
num_clusters = 5
kmeans = MiniBatchKMeans(n_clusters=num_clusters, random_state=42, batch_size=100)
df['cluster'] = kmeans.fit_predict(tfidf_matrix)

print("每篇文章所属的簇：")
print(df[['ID', 'cluster']].head())

# 使用 PCA 降维到 2 维
pca = PCA(n_components=2, random_state=42)
principal_components = pca.fit_transform(tfidf_matrix.toarray())
df['PC1'] = principal_components[:, 0]
df['PC2'] = principal_components[:, 1]

# 绘制 PCA 散点图
plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='PC1', y='PC2',
    hue='cluster',
    palette='viridis',
    data=df,
    legend='full',
    alpha=0.7
)
plt.title('PCA of TF-IDF Vectors')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='Cluster')
plt.show()

# 使用 t-SNE 降维到 2 维
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=300)
tsne_results = tsne.fit_transform(tfidf_matrix.toarray())
df['TSNE1'] = tsne_results[:, 0]
df['TSNE2'] = tsne_results[:, 1]

# 绘制 t-SNE 散点图
plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='TSNE1', y='TSNE2',
    hue='cluster',
    palette='viridis',
    data=df,
    legend='full',
    alpha=0.7
)
plt.title('t-SNE of TF-IDF Vectors')
plt.xlabel('TSNE Component 1')
plt.ylabel('TSNE Component 2')
plt.legend(title='Cluster')
plt.show()
