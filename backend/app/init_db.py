import ast

import pandas as pd
from .database.queries import Queries
from .database.models import Book, BookVector
from .utils.database import Connect_to_database
from .utils.logging_utils import setup_logger
from .utils.file_operations import read_csv
from tqdm import tqdm

if __name__ == "__main__":
    # setup logger
    logger = setup_logger("initiate_database")

    # connect to database
    logger.info("Connecting to the database")
    db_connection = Connect_to_database()

    # get data from the csv file
    logger.info("Reading the saved file")
    data = pd.read_json("/data/preprocessed_data.json", orient="records", lines=True)

    # Save the data in the database respectively.
    logger.info("Inserting the data into the database")
    queryHandler = Queries(db_connection)
    for _, row in tqdm(data.iterrows(), total=data.shape[0], desc="Inserting data"):
        book = Book(
            id=row["id"],
            issued=row["Issued"],
            title=row["Title"],
            language=row["Language"],
            authors=row["Authors"],
            subjects=row["Subjects"],
            bookshelves=row["Bookshelves"],
            cover_url=f"https://www.gutenberg.org/cache/epub/{row["id"]}/{row["id"]}-cover.png",
        )
        queryHandler.insert(book)

    data = None
    logger.info("Reading the saved file")
    data = pd.read_json("/data/content_vectors.json", orient="records", lines=True)
    data["subject_vector"] = pd.read_json(
        "/data/subject_vectors.json", orient="records", lines=True
    )["subject_vector"]
    for _, row in tqdm(data.iterrows(), total=data.shape[0], desc="Inserting data"):
        book_vector = BookVector(
            id=row["id"],
            subject_vector=row["subject_vector"],
            content_vector=row["content_vector"],
        )
        queryHandler.insert(book_vector)

    # close the database connection
    db_connection.close()
