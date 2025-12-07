import numpy as np
from sklearn.cluster import KMeans
from typing import List


def determine_top_n_semantic(
    sentence_embeddings: List[List[float]], min_n: int = 10, max_n: int = 25
) -> int:
    if not sentence_embeddings:
        return min_n
    vectors = np.array(sentence_embeddings)
    N_sentences = len(vectors)
    K = max(3, int(np.sqrt(N_sentences)))

    try:
        kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
        kmeans.fit(vectors)
        base_keywords_per_cluster = 2
        N_recommended = K * base_keywords_per_cluster

        return min(max(N_recommended, min_n), max_n)

    except ValueError:
        return min_n
