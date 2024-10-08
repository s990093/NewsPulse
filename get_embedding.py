import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
import jieba
from gensim import corpora
from gensim.models import LdaModel

# 下载 NLTK 的停用词列表（如未下载）
nltk.download('stopwords')
nltk.download('punkt')

# 加载自定义停用词
def load_stopwords():
    with open("stopwords_zhTW.txt", 'r', encoding='utf-8') as f:
        stop_words = set([line.strip() for line in f])
    return stop_words

# 停用词过滤函数
def remove_stop_words(text):
    words = word_tokenize(text)  # 进行分词
    filtered_words = [word for word in words if word not in stop_words]  # 过滤停用词
    return " ".join(filtered_words)

# 文本预处理函数
def preprocess(text):
    words = jieba.cut(text)
    return [word for word in words if word not in stop_words]

# 文件路径
file_path = 'data/csv/report.csv'  
df = pd.read_csv(file_path)

# 设置停用词
stop_words = load_stopwords()

# 提取文档
documents = df['summary_report'].tolist()

documents_filtered = [remove_stop_words(doc) for doc in documents]

# 对所有文档进行预处理
processed_docs = [preprocess(doc) for doc in documents]

# 创建字典
dictionary = corpora.Dictionary(processed_docs)

# 创建语料库
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# 训练 LDA 模型，设置主题数量
num_topics = 5  # 根据需要调整主题数量
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

# 输出主题信息并获取文档主题
doc_topics = [max(lda_model.get_document_topics(corpus[i]), key=lambda x: x[1])[0] for i in range(len(corpus))]

# 加载 BERT 模型和 Tokenizer
tokenizer = AutoTokenizer.from_pretrained("hw2942/bert-base-chinese-finetuning-financial-news-sentiment-v2")
model = AutoModel.from_pretrained("hw2942/bert-base-chinese-finetuning-financial-news-sentiment-v2")

# 设置为评估模式
model.eval()

# 计算文本的嵌入
def get_embeddings(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()  # 使用 [CLS] token 的向量作为句子表示
    return embeddings

# 筛选相同主题的文档
topic_groups = {}
for idx, topic in enumerate(doc_topics):
    if topic not in topic_groups:
        topic_groups[topic] = []
    topic_groups[topic].append(idx)

# 计算每个主题下文档之间的相似度
similarity_results = []

for topic, indices in topic_groups.items():
    embeddings = get_embeddings([documents_filtered[i] for i in indices])
    
    # 计算余弦相似度
    cos_sim = np.dot(embeddings, embeddings.T) / (np.linalg.norm(embeddings, axis=1, keepdims=True) * np.linalg.norm(embeddings, axis=1, keepdims=True).T)

    # 获取最高相似度的文档对
    for i in range(len(cos_sim)):
        for j in range(i + 1, len(cos_sim)):
            similarity_results.append((indices[i], indices[j], cos_sim[i][j]))

# 按相似度排序并输出最高的前10个
top_similarities = sorted(similarity_results, key=lambda x: x[2], reverse=True)[:10]

# 打印最高的相似度对及其文档内容
for i, (doc1, doc2, sim) in enumerate(top_similarities, 1):
    print(f"Top {i}:")
    print(f"Document {doc1} (ID {df['summary_report'].index[doc1]}): {df['summary_report'].iloc[doc1]}")
    print(f"Document {doc2} (ID {df['summary_report'].index[doc2]}): {df['summary_report'].iloc[doc2]}")
    print(f"Cosine Similarity: {sim:.4f}\n")