from typing import List
from flask import Blueprint, request, jsonify
from ..utils.text_processing import TextProcessor
from ..types import InputText


bp = Blueprint("suggestion", __name__)

# TODO: get the embeddings of the books from database
model = TextProcessor([])


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

        books_id: List[int] = model.most_similar(text)  # get the most similar books

        return jsonify(books_id)
    except:
        return "Internal server error", 500
