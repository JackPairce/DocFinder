FROM python:3.12-slim

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir sentence-transformers sqlalchemy psycopg2-binary pandas numpy flask faiss-cpu

RUN make init

CMD ["make", "run"]
