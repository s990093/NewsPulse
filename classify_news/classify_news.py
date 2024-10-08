from multiprocessing import freeze_support
import jieba
from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
from tqdm import tqdm
from sklearn.metrics import silhouette_score
from sklearn.model_selection import KFold

from get_vectors import *
from cross import kmeans_cross_validation
from rich.progress import Progress

def load_data(file_path):
    """Load CSV data."""
    return pd.read_csv(file_path)

def tokenize(news_data):
    """Tokenize Chinese news data."""
    
    return [doc.split('/') for doc in news_data]

def create_corpus(tokenized_news):
    """Create Gensim dictionary and corpus from tokenized news data."""
    dictionary = corpora.Dictionary(tokenized_news)
    corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_news, desc="Creating corpus")]
    return dictionary, corpus

def train_lda(corpus, dictionary, tokenized_news, num_topics):
    """Train LDA model and return coherence score."""
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    coherence_model = CoherenceModel(model=lda_model, texts=tokenized_news, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    return lda_model, coherence_score

def compute_tfidf(tokenized_news):
    """Compute TF-IDF weights for tokenized news data."""
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
    tfidf_matrix = vectorizer.fit_transform(tokenized_news)
    return pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())


def compute_dfidfo(corpus, lda_model, num_topics, dictionary):
    """Compute DFIDFO weights from LDA topic distribution."""
    topic_word_freq = np.zeros((num_topics, len(dictionary)))

    with Progress() as progress:
        task = progress.add_task("Calculating DFIDFO", total=len(corpus))
        
        for doc_bow, doc_topics in zip(corpus, lda_model.get_document_topics(corpus, minimum_probability=0)):
            for topic_num, prob in doc_topics:
                for word_id, freq in doc_bow:
                    topic_word_freq[topic_num][word_id] += freq * prob
            
            progress.update(task, advance=1)  # Update progress after each document is processed
            
    return topic_word_freq / topic_word_freq.sum(axis=1, keepdims=True)


def combine_weights(tfidf_df, dfidfo_series, alpha=0.7):
    """Combine TF-IDF and DFIDFO weights."""
    combined_weights = tfidf_df.copy()
    for word in tfidf_df.columns:
        if word in dfidfo_series:
            combined_weights[word] = alpha * tfidf_df[word] + (1 - alpha) * dfidfo_series[word]
    return combined_weights

def perform_clustering(reduced_matrix, num_topics):
    """Perform KMeans clustering and return optimal cluster count."""
    silhouette_scores = []
    for n_clusters in range(2, 15):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(reduced_matrix)
        score = silhouette_score(reduced_matrix, kmeans.labels_)
        silhouette_scores.append(score)
    optimal_clusters = silhouette_scores.index(max(silhouette_scores)) + 2
    return optimal_clusters

def plot_results(reduced_matrix, labels, df, show_ids):
    """Plot KMeans clustering results."""
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(reduced_matrix[:, 0], reduced_matrix[:, 1], c=labels, cmap='viridis', alpha=0.6)
    for i, news_id in enumerate(df['news_id']):
        if news_id in show_ids:
            plt.text(reduced_matrix[i, 0], reduced_matrix[i, 1], str(news_id), fontsize=9, ha='right')
    plt.title('KMeans Clustering')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(*scatter.legend_elements(), title="Classes")
    plt.tight_layout()
    plt.show()

def main():
    file_path = 'report.csv'
    df = load_data(file_path)
    news_data = df['FinNA'].tolist()
    news_id = df['news_id'].tolist() 
    
    # Tokenization and corpus creation
    tokenized_news = tokenize(news_data)
    dictionary, corpus = create_corpus(tokenized_news)
    
    # Train LDA model and get coherence score
    num_topics = 5
    lda_model, coherence_score = train_lda(corpus, dictionary, tokenized_news, num_topics)
    print(f"Coherence Score: {coherence_score}")
    
    # Compute TF-IDF and DFIDFO weights
    tfidf_df = compute_tfidf(tokenized_news)
    dfidfo_weights = compute_dfidfo(corpus, lda_model, num_topics, dictionary)
    dfidfo_series = pd.Series(dfidfo_weights.mean(axis=0), index=dictionary.token2id.keys())
    
    # Combine weights
    combined_weights = combine_weights(tfidf_df, dfidfo_series)
    
    # Get embeddings
    word2vec_vectors = get_Word2Vec_embedding(tokenized_news)
    bert_vectors = get_bert_embedding(tokenized_news)
    fasttext_vectors = get_fasttext_embedding(tokenized_news)
    
    combined_vectors = np.hstack([combined_weights.values, word2vec_vectors, bert_vectors, fasttext_vectors])
    
    # PCA and clustering
    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(combined_vectors)
    kmeans = KMeans(n_clusters=num_topics, random_state=42)
    kmeans.fit(reduced_matrix)
    labels = kmeans.labels_
    
    optimal_clusters = perform_clustering(reduced_matrix, num_topics)
    print(f"Optimal Cluster Count: {optimal_clusters}")
    
    results_df = pd.DataFrame({
        'ID': news_id,
        '新聞': news_data,
        '類別': labels
    })
    
    results_df.to_csv("classify_news.csv", index=False)

    show_ids = [407, 383, 392, 384]
    plot_results(reduced_matrix, labels, df, show_ids)

if __name__ == '__main__':
    freeze_support()
    main()
