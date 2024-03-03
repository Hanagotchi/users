FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE ${PORT}

COPY app/ ./

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "${PORT}"]