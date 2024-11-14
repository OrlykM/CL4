FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask mysql-connector-python flask-cors


EXPOSE 5000

CMD ["python", "backend.py"]
