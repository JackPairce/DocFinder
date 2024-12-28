from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    language = Column(String, nullable=False)
    authors = Column(String, nullable=True)
    issued = Column(String, nullable=True)

    # Relationships
    vectors = relationship("BookVector", back_populates="book", uselist=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', language='{self.language}')>"


class BookVector(Base):
    __tablename__ = "book_vectors"

    id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    subjects_vector = Column(Text, nullable=False)  # Serialized vector for subjects
    content_vector = Column(Text, nullable=False)  # Serialized vector for content

    # Relationships
    book = relationship("Book", back_populates="vectors")

    def __repr__(self):
        return f"<BookVector(id={self.id})>"
