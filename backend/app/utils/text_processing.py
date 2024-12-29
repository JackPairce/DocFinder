import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import faiss


class TextProcessor:
    def __init__(
        self, doc_embedding: np.ndarray, metadata_embedding: np.ndarray
    ) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.doc_index = self.init_faiss_index(doc_embedding)
        self.metadata_index = self.init_faiss_index(metadata_embedding)

    def init_faiss_index(self, embedding: np.ndarray) -> faiss.IndexFlatL2:
        dimention = len(embedding[0])
        index = faiss.IndexFlatL2(dimention)
        faiss.normalize_L2(embedding)
        index.add(embedding.astype(np.float32))
        return index

    def most_similar(self, query: str, K=100) -> List[int]:
        query_embedding: np.ndarray = self.model.encode([query])  # type: ignore
        faiss.normalize_L2(query_embedding)
        doc_dist, doc_indices = self.doc_index.search(query_embedding, k=K)  # type: ignore
        metadata_dist, metadata_indices = self.metadata_index.search(query_embedding, k=K)  # type: ignore

        doc_indices = doc_indices[0]
        metadata_indices = metadata_indices[0]
        doc_dist = doc_dist[0]
        metadata_dist = metadata_dist[0]
        print(f"doc_dist: {doc_dist}")
        print(f"metadata_dist: {metadata_dist}")
        doc_indices = doc_indices[doc_dist[doc_dist > 1].argsort()]
        metadata_indices = metadata_indices[metadata_dist[metadata_dist > 1].argsort()]
        # choose the best index
        if len(doc_indices) == 0 or doc_dist.mean() > metadata_dist.mean():
            return metadata_indices[
                doc_dist[doc_dist > doc_dist.mean()].argsort()
            ].tolist()
        if len(metadata_indices) == 0 or doc_dist.mean() < metadata_dist.mean():
            return doc_indices[
                metadata_dist[metadata_dist > metadata_dist.mean()].argsort()
            ].tolist()
        else:
            # combine the two indices
            return np.concatenate([doc_indices[:3], metadata_indices[:2]]).tolist()


def process_text(text: str | List[str]) -> List[float] | List[List[float]]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()  # type: ignore


def process_content(content: str) -> str:
    """
    Extracts the main content of the book, removing the bonus content.

    Args:
        content (str): The full text of the book.

    Returns:
        str: The main content of the book without the bonus content.
    """
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index != -1:
        # Move to the end of the start marker line
        start_index = content.find("\n", start_index) + 1

    if end_index != -1:
        # Get content before the end marker line
        content = content[:end_index]

    return content[start_index:] if start_index != -1 else content


def comparer_similarites(vecteur1, vecteur2, poids=None):
    # Vérification des tailles des vecteurs
    if vecteur1.shape != vecteur2.shape:
        raise ValueError("Les vecteurs doivent avoir la même dimension.")

    # Méthodes de similarité
    def similarite_cosinus(v1, v2):
        norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(v1, v2) / (norm1 * norm2)

    def similarite_euclidienne_inversee(v1, v2):
        distance = np.linalg.norm(v1 - v2)
        return 1 / (1 + distance)

    def similarite_manhattan_inversee(v1, v2):
        distance = np.sum(np.abs(v1 - v2))
        return 1 / (1 + distance)

    def similarite_minkowski_inversee(v1, v2, p=3):
        distance = np.sum(np.abs(v1 - v2) ** p) ** (1 / p)
        return 1 / (1 + distance)

    def similarite_tanimoto(v1, v2):
        dot_product = np.dot(v1, v2)
        norm1, norm2 = np.sum(v1**2), np.sum(v2**2)
        denominator = norm1 + norm2 - dot_product
        if denominator == 0:
            return 0.0
        return dot_product / denominator

    def similarite_correlation(v1, v2):
        if np.std(v1) == 0 or np.std(v2) == 0:
            return 0.0
        return np.corrcoef(v1, v2)[0, 1]

    def similarite_ponderee(v1, v2, w):
        if w is None:
            w = np.ones_like(v1)
        w = w / np.sum(w)
        return similarite_cosinus(v1 * w, v2 * w)

    # Calcul des scores pour chaque méthode
    scores = {
        "similarite_cosinus": similarite_cosinus(vecteur1, vecteur2),
        "similarite_euclidienne_inversee": similarite_euclidienne_inversee(
            vecteur1, vecteur2
        ),
        "similarite_manhattan_inversee": similarite_manhattan_inversee(
            vecteur1, vecteur2
        ),
        "similarite_minkowski_inversee": similarite_minkowski_inversee(
            vecteur1, vecteur2
        ),
        "similarite_tanimoto": similarite_tanimoto(vecteur1, vecteur2),
        "similarite_correlation": similarite_correlation(vecteur1, vecteur2),
    }

    if poids is not None:
        scores["similarite_ponderee"] = similarite_ponderee(vecteur1, vecteur2, poids)

    # Identifier la meilleure méthode (score maximum)
    meilleure_methode = max(scores, key=scores.get)
    return {
        "scores": scores,
        "meilleure_methode": meilleure_methode,
        "meilleur_score": scores[meilleure_methode],
    }
