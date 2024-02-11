FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

COPY app/ ./

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]