FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Исполняем установку с использованием официального кэша pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

ENV TORCH_HOME=/app/.cache/torch
RUN mkdir -p /app/.cache/torch

COPY app.py .
COPY static ./static

EXPOSE 8000

CMD ["python", "app.py"]
