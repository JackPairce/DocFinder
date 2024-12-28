from typing import List
from flask import Blueprint, request, jsonify
from ..utils.text_processing import TextProcessor
from ..utils.database import Connect_to_database
from ..database.queries import Queries
from ..database.models import BookVector
from typing import TypedDict, Literal


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
print(f"{books_embedding = }")

book_embedding_model = TextProcessor(books_embedding)


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

        books_id: List[int] = [1, 2, 3]
        # books_id: List[int] = book_embedding_model.most_similar(
        #     text
        # )  # get the most similar books

        return jsonify(books_id)
    except:
        return "Internal server error", 500

class InputText(TypedDict):
    Text: str


Language = Literal["english", "french"]