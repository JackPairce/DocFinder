import ast
import os

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
    logger.info("Reading metadata from the CSV file")
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
    logger.info("Reading the subject and content vectors from the files")
    # read directory "/data/subject_vectors" and "/data/content_vectors" and insert the data into the database
    files = os.listdir("/data/subject_vectors")
    for file in tqdm(files, desc="Inserting data"):
        data = pd.read_json(
            f"/data/subject_vectors/{file}", orient="records", lines=True
        )
        data["content_vector"] = pd.read_json(
            f"/data/content_vectors/{file}", orient="records", lines=True
        )["content_vector"]
        for _, row in data.iterrows():
            book_vector = BookVector(
                id=row["id"],
                subject_vector=row["subject_vector"],
                content_vector=row["content_vector"],
            )
            queryHandler.insert(book_vector)

    # delete all files in the directory
    logger.info("Deleting the saved files")
    os.system("rm -r /data/subject_vectors")
    os.system("rm -r /data/content_vectors")
    os.system("rm /data/preprocessed_data.json")

    # close the database connection
    db_connection.close()
