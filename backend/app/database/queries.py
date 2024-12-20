from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.base import Base


class Queries:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, new_data: Base):
        try:
            self.session.add(new_data)
            self.session.commit()
            return new_data
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to insert data: {e}")

    def get_id(self, model: Base, id: int):
        try:
            data = self.session.query(model).filter_by(id=id).first()
            return data
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get data: {e}")

    def update(self, model: Base, id: int, new_data: dict):
        try:
            data = self.get_id(model, id)
            if data:
                for key, value in new_data.items():
                    setattr(data, key, value)
                self.session.commit()
                return data
            else:
                raise Exception(f"Data with id {id} not found")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to update data: {e}")

    def get_all(self, model: Base):
        try:
            data = self.session.query(model).all()
            return data
        except SQLAlchemyError as e:
            raise Exception(f"Failed to get data: {e}")
