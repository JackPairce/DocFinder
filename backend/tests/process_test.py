import unittest

from numpy import ndarray
from backend.app.utils.file_operations import get_book_by_id
from backend.app.utils.text_processing import process_text, TextProcessor
import random
import numpy as np


class TestProcess(unittest.TestCase):
    # def test_get_book_by_id(self):
    #     id = random.randint(1, 100)
    #     book = get_book_by_id(id)
    #     self.assertIsInstance(book, str)
    #     self.assertGreater(len(book), 0)

    # def test_process_text(self):
    #     book = get_book_by_id(1)
    #     embeddings = process_text(book)
    #     self.assertIsInstance(embeddings, ndarray)
    #     self.assertGreater(len(embeddings), 0)

    def test_suggestion(self):
        author = "Abraham Lincoln"
        query = f"I want a book wrote by {author}"
        ids = list(range(1, 20))

        books = [get_book_by_id(id) for id in ids]

        target_books_id = [id for id, bk in enumerate(books) if author in bk]

        books_embeddings = [process_text(book) for book in books]
        most_similary_ids = TextProcessor(books_embeddings).most_similar(query, 0.5)
        print(f"{most_similary_ids = }, {target_books_id = }")
        self.assertIsInstance(most_similary_ids, list)
        self.assertEqual(most_similary_ids, target_books_id)

    def test_suggestion2(self):
        target = "I therefore consider that, in view of the Constitution and the laws"
        # query = f"find a book that contains the following text: {target}"
        query = target
        ids = list(range(1, 20))
        books = [get_book_by_id(id) for id in ids]
        books = [bk.split("***")[2] for bk in books]
        target_books_id = [id for id, bk in enumerate(books) if target in bk]
        books_embeddings = [process_text(book) for book in books]
        most_similary_ids = TextProcessor(books_embeddings).most_similar(query)
        print(f"{most_similary_ids = }, {target_books_id = }")
        self.assertIsInstance(most_similary_ids, list)
        self.assertEqual(most_similary_ids, target_books_id)


if __name__ == "__main__":
    unittest.main()
