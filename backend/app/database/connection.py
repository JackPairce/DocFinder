from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError


class Connection:
    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.engine = None
        self.SessionLocal = None

    def connect(self) -> None:
        try:
            connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
            self.engine = create_engine(connection_string)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            print("Connected to database")
        except OperationalError as e:
            print(f"Failing to connect to database: {e}")
            self.engine = None

    def close(self) -> None:
        if self.engine:
            self.engine.dispose()
            print("Connection closed")

    def get_session(self):
        if self.SessionLocal is None:
            raise ConnectionError("Database connection is not established")
        return self.SessionLocal()
