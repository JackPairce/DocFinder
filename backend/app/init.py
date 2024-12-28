import os
from database.queries import Queries
from database.models import Book, BookVector
from database.connection import Connection
from utils.file_operations import download_file, read_csv
from utils.text_processing import process_text
from utils.file_operations import get_book_by_id


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
        7. use Sentence Transformers (all-MiniLM-L6-v2) to encode the "subject_vector" column and save it on same column.
        8. for each book id get book contents (using get_book_id from file_operations) and encode it using Sentence Transformers (all-MiniLM-L6-v2) and save it in the column "Book_content_vector".
        9. Save the data in the database respectively.

    Tips:
        - Use the `pandas` library to manipulate the data.
        - Use the `transformers` library to encode the text.
        - Use the `psycopg2` library to connect to the database
        - Use the `tqdm` library to display a progress bar.
        - Don't forget to close the database connection when you are done.
        - Make sure to handle any exceptions that may occur.
        - Use logging each step done (you can use the `setup_logger` function from the `logging_utils` module).
    """
    #! set up logger

    # connect to database
    connection = Connect_to_database()

    # the link of the csv file
    LNK = os.environ.get("PG_CATALOG")
    if LNK is None:
        raise ValueError("PG_CATALOG is not set")

    CSV_FILE = "/tmp/pg_catalog.csv"
    # download the csv file
    download_file(LNK, CSV_FILE)
    # read the csv file
    data = read_csv(CSV_FILE)
    data.rename(columns={"Text#": "id"}, inplace=True)
    data.drop(columns=["LoCC"], inplace=True)

    # Filter "Type" by "Text" only
    data = data[data["Type"] == "Text"]

    # Filter "Languages" by "en" and "fr", and rename them
    data = data[data["Language"].isin(["en", "fr"])]
    data["Language"] = data["Language"].replace({"en": "english", "fr": "french"})

    # use Sentence Transformers (all-MiniLM-L6-v2) to encode the "subject_vector" column and save it on same column.
    # issued, authors, title, subjects
    data["subject_vector"] = data.apply(
        lambda row: f"{row['issued']} {row['authors']} {row['title']} {row['subjects']} {row['bookshelves']}",
        axis=1,
    )
    data["subject_vector"] = data["subject_vector"].apply(process_text)
    print(data["subject_vector"])

    # for each book id get book contents (using get_book_id from file_operations) and encode it using Sentence Transformers (all-MiniLM-L6-v2) and save it in the column "Book_content_vector".
    data["Book_content_vector"] = data["id"].apply(get_book_by_id)

    # Save the data in the database respectively.
    queryHandler = Queries(db.get_session())
    for _, row in data.iterrows():
        book = Book(
            id=row["id"],
            title=row["title"],
            language=row["Language"],
            authors=row["authors"],
            issued=row["issued"],
        )
        book_vector = BookVector(
            id=row["id"],
            subjects_vector=row["subject_vector"],
            content_vector=row["Book_content_vector"],
        )

        queryHandler.insert(book)
        queryHandler.insert(book_vector)



    ...
