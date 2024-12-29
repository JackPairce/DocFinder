import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


class TextProcessor:
    def __init__(self, doc_embedding: List[np.ndarray]):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents_embeddings = doc_embedding

    def most_similar(self, query: str, P=0.5) -> List[int]:
        query_embedding: np.ndarray = self.model.encode(query)  # type: ignore
        similarity: np.ndarray = cosine_similarity(
            np.array([query_embedding]), np.array(self.documents_embeddings)
        )[0]
        most_similar_index = similarity.argsort()[::-1]
        max_value = similarity[most_similar_index[0]]
        if max_value < P:
            nb = str(max_value).split(".")[1][0]
            P = float(f"0.{nb}")

        most_similar_index = [i for i in most_similar_index if similarity[i] > P]
        return np.array(most_similar_index, dtype=int).tolist()  # type: ignore


def process_text(text: str | List[str]) -> List[float] | List[List[float]]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()  # type: ignore
