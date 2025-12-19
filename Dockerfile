FROM python:3.11-slim

WORKDIR /app

# system deps if needed
RUN apt-get update && apt-get install -y build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# set environment variable for reflex if needed
ENV PORT=8080
EXPOSE 8080

CMD exec gunicorn -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT main:app
