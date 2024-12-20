from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

# Association Table for Books and Bookshelves (Categories)
book_category_association = Table(
    "book_category_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("bookshelves.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    language = Column(String, nullable=False)
    authors = Column(String, nullable=True)
    issued = Column(String, nullable=True)

    # Relationships
    bookshelves = relationship(
        "Bookshelf", secondary=book_category_association, back_populates="books"
    )
    vectors = relationship("BookVector", back_populates="book", uselist=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', language='{self.language}')>"


class Bookshelf(Base):
    __tablename__ = "bookshelves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships
    books = relationship(
        "Book", secondary=book_category_association, back_populates="bookshelves"
    )

    def __repr__(self):
        return f"<Bookshelf(id={self.id}, name='{self.name}')>"


class BookVector(Base):
    __tablename__ = "book_vectors"

    id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    subjects_vector = Column(Text, nullable=False)  # Serialized vector for subjects
    content_vector = Column(Text, nullable=False)  # Serialized vector for content

    # Relationships
    book = relationship("Book", back_populates="vectors")

    def __repr__(self):
        return f"<BookVector(id={self.id})>"
