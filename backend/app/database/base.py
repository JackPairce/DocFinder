from sqlalchemy.orm import DeclarativeBase
from typing import Generic, TypeVar

TBase = TypeVar("TBase", bound="Base")


# Create the declarative base
class Base(DeclarativeBase, Generic[TBase]):
    pass
