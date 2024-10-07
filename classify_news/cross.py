
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


def kmeans_cross_validation(data, num_clusters=3, n_splits=5):
    # Initialize KFold
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    silhouette_scores = []
    
    for train_index, test_index in kf.split(data):
        # Split the data
        X_train, X_test = data[train_index], data[test_index]
        
        # Initialize KMeans
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        
        # Fit the KMeans on training data
        kmeans.fit(X_train)
        
        # Predict clusters on test data
        labels = kmeans.predict(X_test)
        
        # Calculate silhouette score on test data
        score = silhouette_score(X_test, labels)
        silhouette_scores.append(score)
    
    avg_silhouette_score = np.mean(silhouette_scores)
    print(f"Average Silhouette Score across {n_splits} folds: {avg_silhouette_score}")
    return avg_silhouette_score

# Main function adjusted for cross-validation
# def main():
#     # (Your existing code...)
#     # 8. 使用 PCA 降維到 2 維
#     pca = PCA(n_components=2)
#     reduced_matrix = pca.fit_transform(weighted_matrix)
    
#     # Perform cross-validation on KMeans
#     kmeans_cross_validation(reduced_matrix, num_clusters=num_topics, n_splits=5)

