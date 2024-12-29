from ..database.connection import Connection
from sqlalchemy.orm import Session
import os


def Connect_to_database() -> Session:

    # get environment variables
    URL = os.environ.get("DATABASE_URL") or "localhost:5432"
    if URL is None:
        raise ValueError("DATABASE_URL is not set")

    DBNAME = os.environ.get("POSTGRES_DB")
    USER = os.environ.get("POSTGRES_USER")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    HOST, PORT = URL.split(":")

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

    return db.get_session()
