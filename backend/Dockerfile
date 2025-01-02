FROM python:3.12-slim

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir sentence-transformers sqlalchemy psycopg2-binary pandas numpy flask flask_cors faiss-cpu

ARG BOOKS_LIMIT=100

RUN make preprocess

CMD ["make", "run"]
