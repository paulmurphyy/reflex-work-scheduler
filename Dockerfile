FROM python:3.12-slim

# Install Node.js (needed for Reflex frontend compilation)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Cloud Run expects container to listen on $PORT
ENV PORT 8080
EXPOSE 8080

# Start Uvicorn server pointing to Reflex app object
CMD ["uvicorn", "reflex_work_scheduler.reflex_work_scheduler:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]
