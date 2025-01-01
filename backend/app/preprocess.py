import os

from .utils.file_operations import download_file, read_csv
from .utils.text_processing import process_text, process_content
from .utils.file_operations import get_book_by_id
from .utils.logging_utils import setup_logger
from tqdm import tqdm

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
    # setup logger
    logger = setup_logger("preprocess")

    # the link of the csv file
    logger.info("Downloading the CSV file")
    LNK = os.environ.get("PG_CATALOG")
    if LNK is None:
        raise ValueError("PG_CATALOG is not set")

    CSV_FILE = "/tmp/pg_catalog.csv"
    # download the csv file
    download_file(LNK, CSV_FILE)

    # read the csv file
    logger.info("Reading the CSV file")
    data = read_csv(CSV_FILE)

    # rename column Text# to id and delete column LoCC
    data.rename(columns={"Text#": "id"}, inplace=True)
    data.drop(columns=["LoCC"], inplace=True)

    # Filter "Type" by "Text" only
    logger.info("Filtering the data by 'Type' column")
    data = data[data["Type"] == "Text"]

    # Filter "Languages" by "en" and "fr", and rename them
    logger.info("Filtering the data by 'Language' column")
    data = data[data["Language"].isin(["en", "fr"])]
    data["Language"] = data["Language"].replace({"en": "english", "fr": "french"})

    # process Authors and Bookshelves columns
    # split the Authors and Bookshelves columns by ";" and remove date from the Authors column then split it by "," and join it by " ".
    data["Authors"] = (
        data["Authors"].str.replace(r"\d{4}-\d{4}", "").str.replace(",", "").str.strip()
    )
    data["Authors"] = data["Authors"].str.split(";")

    # split the Bookshelves column by ";"
    data["Bookshelves"] = data["Bookshelves"].str.split(";")

    # split the Subjects column by ";"
    data["Subjects"] = data["Subjects"].str.split(";")

    # remove nan values of each row
    data.dropna(inplace=True)

    # user books limit
    ENV_BOOKS_LIMIT = os.environ.get("BOOKS_LIMIT")
    if ENV_BOOKS_LIMIT is None:
        BOOKS_LIMIT = 1000
    elif ENV_BOOKS_LIMIT.isdigit():
        BOOKS_LIMIT = int(ENV_BOOKS_LIMIT)
    elif ENV_BOOKS_LIMIT.lower() == "all":
        BOOKS_LIMIT = data.shape[0]
    else:
        BOOKS_LIMIT = 1000
    CHUNKS_SIZE = 10
    data = data[:BOOKS_LIMIT]
    # use Sentence Transformers (all-MiniLM-L6-v2) to encode the "subject_vector" column and save it on same column.
    # issued, authors, title, subjects
    logger.info("Encoding the  metadata of the books to vectors")
    output = []
    for i in tqdm(
        range(0, data.shape[0], CHUNKS_SIZE),
        total=data.shape[0] // CHUNKS_SIZE,
        desc="Processing data",
    ):
        target = (
            data.iloc[i : i + CHUNKS_SIZE]
            .apply(
                lambda row: f"title:{row["Title"]};authors:{','.join(row["Authors"])};subjects:{','.join(row["Subjects"])};bookshelves:{','.join(row["Bookshelves"])};date:{row["Issued"]}",
                axis=1,
            )
            .tolist()
        )
        output.extend(process_text(target))
    data["subject_vector"] = output

    # for each book id get book contents (using get_book_id from file_operations) and encode it using Sentence Transformers (all-MiniLM-L6-v2) and save it in the column "Book_content_vector".
    logger.info("Encoding the Book content column to vectors")
    output = []
    for i in tqdm(
        range(0, data.shape[0], CHUNKS_SIZE),
        total=data.shape[0] // CHUNKS_SIZE,
        desc="Download and Processing book content",
    ):
        target = (
            data["id"]
            .iloc[i : i + CHUNKS_SIZE]
            .apply(get_book_by_id)
            .apply(process_content)
            .tolist()
        )
        output.extend(process_text(target))
    data["content_vector"] = output

    # save the data in file
    logger.info("Saving the data")
    os.makedirs("/data", exist_ok=True)
    data.to_json("/data/preprocessed_data.json", orient="records", lines=True)
