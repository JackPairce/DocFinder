import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


class TextProcessor:
    def __init__(self, doc_embedding: List[np.ndarray]):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents_embeddings = doc_embedding

    def most_similar(self, query: str, P=0.5) -> List[int]:
        query_embedding = self.model.encode(query).numpy()
        similarity: np.ndarray = cosine_similarity(
            np.array([query_embedding]), np.array(self.documents_embeddings)
        )[0]
        most_similar_index = similarity.argsort()[::-1]
        max_value = similarity[most_similar_index[0]]
        if max_value < P:
            nb = str(max_value).split(".")[1][0]
            P = float(f"0.{nb}")

        most_similar_index = [i for i in most_similar_index if similarity[i] > P]
        return list(np.array(most_similar_index, dtype=int))


def process_text(text: str) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(text).numpy()
    return embeddings

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