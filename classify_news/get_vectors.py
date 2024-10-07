import pandas as pd
from transformers import BertModel, BertTokenizer
import torch
from gensim.models import Word2Vec
import fasttext
from rich.progress import Progress


# 讀取文件
file_path = 'report.csv'
df = pd.read_csv(file_path)

# 提取文本資料
news_data = df['FinNA'].tolist()

# 中文分詞（根據 '/' 分隔）
# def tokenize(text):
#     return text.split('/')

# tokenized_news = [tokenize(doc) for doc in news_data]

# tokenized_news_joined = [' '.join(doc) for doc in tokenized_news]





tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')


def get_Word2Vec_embedding(tokenized_news):
    # 訓練 Word2Vec 模型
    w2v_model = Word2Vec(sentences=tokenized_news, vector_size=100, window=5, min_count=1, workers=4)
    
    word2vec_vectors = []
    # 使用 rich 進度條
    with Progress() as progress:
        task = progress.add_task("Getting Word2Vec embeddings...", total=len(tokenized_news))
        for doc in tokenized_news:
            vector = w2v_model.wv[doc].mean(axis=0)
            word2vec_vectors.append(vector)
            progress.update(task, advance=1)
    
    return word2vec_vectors




# 將每篇文檔轉為 BERT 嵌入
def get_bert_embedding(tokenized_news):
    def _embedding(text):
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    bert_vectors = []
    # 使用 rich 進度條
    with Progress() as progress:
        task = progress.add_task("Getting BERT embeddings...", total=len(tokenized_news))
        for doc in tokenized_news:
            vector = _embedding(' '.join(doc))
            bert_vectors.append(vector)
            progress.update(task, advance=1)
    
    return bert_vectors


def get_fasttext_embedding(tokenized_news):
    # 將 tokenized_news 保存到一個臨時文件中
    with open('news_corpus.txt', 'w', encoding='utf-8') as f:
        for doc in tokenized_news:
            f.write(' '.join(doc) + '\n')  # 每篇文檔寫成一行

    # 使用該文件來訓練 FastText 模型
    fasttext_model = fasttext.train_unsupervised('news_corpus.txt', model='skipgram')

    fasttext_vectors = []
    # 使用 rich 進度條
    with Progress() as progress:
        task = progress.add_task("Getting FastText embeddings...", total=len(tokenized_news))
        for doc in tokenized_news:
            vector = fasttext_model.get_sentence_vector(' '.join(doc))
            fasttext_vectors.append(vector)
            progress.update(task, advance=1)
    
    return fasttext_vectors

# import numpy as np

# 將所有特徵向量進行拼接
# combined_vectors = np.hstack([tfidf_vectors.toarray(), word2vec_vectors, bert_vectors, fasttext_vectors])





# 假設 combined_vectors 是你之前計算的聚類向量
# 設定 KMeans 聚類

# num_topics = 5  # 設定聚類數目，可以根據您的需求調整

# # 8. 使用 PCA 降維到 2 維
# pca = PCA(n_components=2)
# reduced_matrix = pca.fit_transform(combined_vectors)

# # 9. KMeans 聚類
# kmeans = KMeans(n_clusters=num_topics, random_state=42)
# kmeans.fit(reduced_matrix)
# labels = kmeans.labels_

# # 進行多次 KMeans 以選擇最佳的聚類數
# silhouette_scores = []
# for n_clusters in range(2, 15):
#     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#     kmeans.fit(reduced_matrix)
#     score = silhouette_score(reduced_matrix, kmeans.labels_)
#     silhouette_scores.append(score)

# optimal_clusters = silhouette_scores.index(max(silhouette_scores)) + 2
# print(f"最佳聚類數: {optimal_clusters}")

# # 使用 DataFrame 以更友好的方式展示結果
# results_df = pd.DataFrame({
#     '新聞': news_data,
#     '類別': labels
# })


# # 特別顯示的 news_id
# show_ids = [407, 383, 392, 384]

# # 繪製 KMeans 聚類結果的 2D 散點圖
# plt.figure(figsize=(10, 6))
# scatter = plt.scatter(reduced_matrix[:, 0], reduced_matrix[:, 1], c=labels, cmap='viridis', alpha=0.6)

# # 在指定的點上顯示對應的 news_id
# for i, news_id in enumerate(df['news_id']):
#     if news_id in show_ids:  # 只顯示指定的 news_id
#         print(news_id)
#         plt.text(reduced_matrix[i, 0], reduced_matrix[i, 1], str(news_id), fontsize=9, ha='right')


# # 添加標題和標籤
# plt.title('KMeans ')
# plt.xlabel('x')
# plt.ylabel('y')

# # 創建顏色條
# legend1 = plt.legend(*scatter.legend_elements(), title="類別")
# plt.gca().add_artist(legend1)

# # 顯示圖形
# plt.tight_layout()
# plt.show()