from typing import List
import os
import nltk
from database.connection import Connection
from utils.file_operations import download_file
from utils.file_operations import read_csv

if __name__ == "__main__":
    """
    Main entry point for initializing the database.

    content of the CSV file:
    [  Text#	Type	Issued	Title	Language	Authors	Subjects	LoCC	Bookshelves	]

    TODO:
        1. Download the CSV file.
        2. load the CSV file.
        3. rename column Text# to id
        4. Delete column  LoCC
        5. Filter "Type" by "Text" only
        6. Filter "Languages" by "en" and "fr" only and rename "en" to 'english' and "fr" to 'french'
        7. Bookshelves column contains a list of bookshelves separated by ';'. Split the column into a list of bookshelves and store it in a new column called "Bookshelves_vector".
        8. Tokenize the "Booksheves_vector" column and save it on same column.
        9. use Sentence Transformers (all-MiniLM-L6-v2) to encode the "Bookshelves_vector" column and save it on same column.
        10. Save the data in the database respectively.

    Tips:
        - Use the `pandas` library to manipulate the data.
        - Use the `nltk` library to tokenize the text.
        - Use the `transformers` library to encode the text.
        - Use the `psycopg2` library to connect to the database
        - Use the `tqdm` library to display a progress bar.
        - Don't forget to close the database connection when you are done.
        - Make sure to handle any exceptions that may occur.
        - Use logging each step done (you can use the `setup_logger` function from the `logging_utils` module).
    """
    # download nltk data
    nltk.download("punkt")
    nltk.download("stopwords")

    #! set up logger

    # get environment variables
    URL = os.environ.get("DATABASE_URL")
    if URL is None:
        raise ValueError("DATABASE_URL is not set")

    DBNAME = os.environ.get("POSTGRES_DB")
    USER = os.environ.get("POSTGRES_USER")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    HOST, PORT = URL.split(":")

    # the link of the csv file
    LNK = os.environ.get("PG_CATALOG")
    if LNK is None:
        raise ValueError("PG_CATALOG is not set")

    if DBNAME is None or USER is None or PASSWORD is None:
        raise ValueError("Invalid DATABASE_URL")

    # connect to the database
    db = Connection(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=int(PORT),
    )
    db.connect()

    CSV_FILE = "/tmp/pg_catalog.csv"
    # download the csv file
    download_file(LNK, CSV_FILE)
    # read the csv file
    data = read_csv(CSV_FILE)

    ...
