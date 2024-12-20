FROM python:3.13-slim

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY . .

RUN make init

CMD ["make", "run"]
