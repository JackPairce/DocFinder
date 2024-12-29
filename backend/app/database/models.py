from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT, DATE, TEXT, INTEGER
from .base import Base


class Book(Base["Book"]):
    __tablename__ = "books"

    id = Column(INTEGER, primary_key=True)
    issued = Column(DATE)
    title = Column(TEXT, nullable=False)
    language = Column(TEXT)
    authors = Column(ARRAY(TEXT))
    subjects = Column(ARRAY(TEXT))
    bookshelves = Column(ARRAY(TEXT))
    cover_url = Column(TEXT)

    # Relationships
    vectors = relationship("BookVector", back_populates="book", uselist=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"


class BookVector(Base["BookVector"]):
    __tablename__ = "books_vectors"

    id = Column(INTEGER, ForeignKey("books.id"), primary_key=True)
    subject_vector = Column(
        ARRAY(FLOAT), nullable=False
    )  # Serialized vector for subjects
    content_vector = Column(
        ARRAY(FLOAT), nullable=False
    )  # Serialized vector for content

    # Relationships
    book = relationship("Book", back_populates="vectors")

    def __repr__(self):
        return f"<BookVector(id={self.id})>"
