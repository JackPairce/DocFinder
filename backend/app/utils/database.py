from database.queries import Queries
from database.models import Book
from database.connection import Connection


def test_insert_data():
    # connect to database
    conn = Connection(dbname="testdb", user="testuser", password="testpass")
    conn.connect()
    session = conn.get_session()

    # insert data
    book = Book(title="Test Book", author="Test Author")
    Queries(session).insert(book)
