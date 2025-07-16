FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    pip install Flask pdfkit

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
