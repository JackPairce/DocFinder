FROM python:3.13-slim-bullseye

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir sentence-transformers sqlalchemy spycopg2-binary pandas numpy flask

RUN make init

CMD ["make", "dev"]
