FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

# Use CMD so Cloud Run can override if needed
CMD ["reflex", "start", "--env", "prod", "--port", "8080", "--loglevel", "debug"]