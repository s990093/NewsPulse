import gensim
from gensim import corpora
from nltk.corpus import stopwords
import string
import jieba
import pyLDAvis
import pyLDAvis.gensim_models
import pandas as pd

# 加載中文停用詞
stop_words = set(stopwords.words('chinese'))
file_path = 'data/csv/report.csv'  
df = pd.read_csv(file_path)

source = "extracted_news_info"
# 2. 标签分割
df['tags'] = df[source].apply(lambda x: x.split('/'))



# 3. 將 tags 列展平為文本數據
df['tags'] = df['tags'].apply(lambda x: ' '.join(x))

# 4. 使用 jieba 進行分詞
def preprocess(text):
    return list(jieba.cut(text))

# 5. 對所有文本進行分詞
processed_docs = df['tags'].apply(preprocess)

# 6. 創建詞典和語料庫
dictionary = corpora.Dictionary(processed_docs)
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# 7. 訓練 LDA 模型
lda_model = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=8, passes=10)

# 8. 查看每個主題中的關鍵詞
print("每個主題中的關鍵詞:")
for idx, topic in lda_model.print_topics(-1):
    print(f"主題 {idx}: {topic}")

# 9. 繪製主題模型的視覺化
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# 10. 將視覺化結果保存到 HTML 文件
pyLDAvis.save_html(vis, 'lda_visualization.html')

print("\nLDA 視覺化已保存至 'lda_visualization.html'。")




