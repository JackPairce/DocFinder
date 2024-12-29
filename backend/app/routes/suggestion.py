from typing import List
from flask import Blueprint, request, jsonify
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

book_embedding_model = TextProcessor([book.content_vector for book in books_embedding])  # type: ignore


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

        # get the most similar books
        books_index: List[int] = book_embedding_model.most_similar(text)

        #
        books_ids = [books_embedding[id].id for id in books_index]

        return json.dumps({"Books": books_ids}), 200
    except Exception as e:
        return f"Internal server error: {e}", 500
