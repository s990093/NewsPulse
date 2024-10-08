import jieba
from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_path = 'report.csv'  
df = pd.read_csv(file_path)

# 1. 準備新聞資料
news_data  = df['FinNA'].tolist()

# 2. 中文分詞（透過 '/' 分隔）
def tokenize(text):
    return text.split('/')

tokenized_news = [tokenize(doc) for doc in news_data]
print("分詞結果:")
for idx, doc in enumerate(tokenized_news):
    print(f"新聞 {idx+1}: {doc}")

# 3. 建立詞典和語料庫
dictionary = corpora.Dictionary(tokenized_news)
corpus = [dictionary.doc2bow(text) for text in tokenized_news]

# 4. LDA 主題分類
num_topics = 10  # 假設分為2個主題，根據資料調整
lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

print("\nLDA 主題分布:")
doc_topics_list = []
for idx, doc_bow in enumerate(corpus):
    doc_topics = lda_model.get_document_topics(doc_bow)
    doc_topics_list.append(doc_topics)
    print(f"新聞 {idx+1} 主題分布: {doc_topics}")

# 5. 計算 TF-IWF
# 使用 TF-IDF 作為近似
tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
tfidf_matrix = tfidf_vectorizer.fit_transform(tokenized_news)
tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_feature_names)
print("\nTF-IWF 權重矩陣:")
print(tfidf_df)

# 6. 計算 DFIDFO
# DFIDFO: 根據 LDA 主題分布計算詞語的類別頻率加權
topic_word_freq = np.zeros((num_topics, len(dictionary)))
for doc_bow, doc_topics in zip(corpus, lda_model.get_document_topics(corpus, minimum_probability=0)):
    for topic_num, prob in doc_topics:
        for word_id, freq in doc_bow:
            topic_word_freq[topic_num][word_id] += freq * prob

# 正規化每個主題的詞頻
topic_word_freq_normalized = topic_word_freq / topic_word_freq.sum(axis=1, keepdims=True)

# 計算每個詞的 DFIDFO 權重
dfidfo_weights = topic_word_freq_normalized.mean(axis=0)
dfidfo_series = pd.Series(dfidfo_weights, index=dictionary.token2id.keys())
print("\nDFIDFO 權重:")
print(dfidfo_series)

# 7. 組合權重
combined_weights = tfidf_df.copy()
for word in tfidf_feature_names:
    if word in dfidfo_series:
        combined_weights[word] = tfidf_df[word] + dfidfo_series[word]
    else:
        combined_weights[word] = tfidf_df[word]

print("\n組合權重矩陣:")
print(combined_weights)

# 將組合權重轉換為 NumPy 矩陣
weighted_matrix = combined_weights.values
print("\n加權矩陣 (NumPy):")
print(weighted_matrix)

# 8. 使用 PCA 降維到 2 維
pca = PCA(n_components=2)
reduced_matrix = pca.fit_transform(weighted_matrix)
print("\n降維後矩陣 (PCA 2維):")
print(reduced_matrix)

# 9. KMeans 聚類
kmeans = KMeans(n_clusters=num_topics, random_state=42)
kmeans.fit(reduced_matrix)
labels = kmeans.labels_

# 輸出每篇新聞的聚類結果
print("\nKMeans 聚類結果:")
for idx, label in enumerate(labels):
    print(f"新聞 {idx+1} ('{news_data[idx]}') 所屬類別: 類別 {label}")

# 使用 DataFrame 以更友好的方式展示結果
results_df = pd.DataFrame({
    '新聞': news_data,
    '類別': labels
})
print("\n聚類結果表:")
print(results_df)

results_df.to_csv("test.csv")

# 10. 可視化 KMeans 聚類結果（PCA後的2D矩陣）
plt.figure(figsize=(10, 6))
scatter = plt.scatter(reduced_matrix[:, 0], reduced_matrix[:, 1], c=labels, cmap='viridis', alpha=0.6)

# 添加標題和標籤
plt.title('KMeans 聚類結果 (PCA 降維)')
plt.xlabel('主成分 1')
plt.ylabel('主成分 2')

# 創建顏色條
legend1 = plt.legend(*scatter.legend_elements(), title="類別")
plt.gca().add_artist(legend1)

# 顯示圖形
plt.tight_layout()
plt.show()

