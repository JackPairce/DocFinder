from typing import List
from flask import Blueprint, request
import numpy as np
from ..utils.text_processing import TextProcessor
from ..utils.database import Connect_to_database
from ..database.queries import Queries
from ..database.models import BookVector
from typing import TypedDict, Literal
import json


class InputText(TypedDict):
    Text: str


Language = Literal["english", "french"]


# create a blueprint
bp = Blueprint("suggestion", __name__)

# connect to database
connection = Connect_to_database()

# get all books vector
query_handler = Queries(connection)
books_embedding = query_handler.get_all(BookVector())

subject_vector = np.array([book.subject_vector for book in books_embedding]).astype(
    np.float32
)
content_vector = np.array([book.content_vector for book in books_embedding]).astype(
    np.float32
)

book_embedding_model = TextProcessor(content_vector, subject_vector)  # type: ignore


@bp.route("/suggest", methods=["POST"])
def suggest():
    """
    This function is a placeholder for the suggestion route.

    Input: InputText {"Text": str}

    Output: List[int]
    """
    try:
        data: InputText = request.get_json()

        if not data or not data["Text"]:
            return "Invalid input", 400

        text = data["Text"]

        K = determine_k(text, len(books_embedding), max_k=10)

        # get the most similar books
        books_index: List[int] = book_embedding_model.most_similar(text, K)

        # get the books ids
        books_ids = [books_embedding[id].id for id in books_index]

        return json.dumps({"Books": books_ids}), 200
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return f"Internal server error: {e}", 500


def determine_k(query, dataset_size, max_k=10):
    """
    Dynamically determine the value of k based on query length and dataset size.

    Arguments:
    - query (str): User input query.
    - dataset_size (int): Total number of items in the dataset.
    - max_k (int): Maximum value for k.

    Returns:
    - int: Optimal value of k.
    """
    # Adjust based on query length
    query_length = len(query.split())  # Number of words in the query
    if query_length < 3:
        k = max_k  # Vague queries, return more results
    else:
        k = max(5, int(max_k * 0.5))  # More specific queries, fewer results

    # Adjust based on dataset size
    if dataset_size < 100:
        k = min(k, 5)  # Small dataset, limit results
    else:
        k = min(k, dataset_size // 10)  # Use 10% of dataset size as a cap

    return k
