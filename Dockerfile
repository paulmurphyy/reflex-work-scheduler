FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Cloud Run expects container to listen on $PORT
ENV PORT 8080
EXPOSE 8080

# Start Uvicorn on the Reflex app
# Module path: reflex-work-scheduler.reflex-work-scheduler
# Python module names cannot have dashes, so we use underscores
CMD ["uvicorn", "reflex_work_scheduler.reflex_work_scheduler:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]