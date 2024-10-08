import pandas as pd

file_path = 'data/csv/report.csv'  
df = pd.read_csv(file_path)
# 假设 df 是你的数据框，包含 summary_report 列
documents = df['summary_report'].tolist()


import jieba

# 加载中文停用词
with open('stopwords_zhTW.txt', 'r', encoding='utf-8') as f:
    stopwords_zh = set(f.read().splitlines())

def preprocess(text):
    # 分词并去除停用词
    words = jieba.cut(text)
    return [word for word in words if word not in stopwords_zh]

# 对所有文档进行预处理
processed_docs = [preprocess(doc) for doc in documents]



from gensim import corpora
from gensim.models import LdaModel

# 创建字典和语料库
dictionary = corpora.Dictionary(processed_docs)
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# 训练 LDA 模型
lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)



# 获取每个文档的主题
doc_topics = []
for doc in corpus:
    topic_distribution = lda_model.get_document_topics(doc)
    doc_topics.append(max(topic_distribution, key=lambda x: x[1])[0])  # 选择概率最大的主题


# print(doc_topics)


lda_model.save("lda_model.model")
