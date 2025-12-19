FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV PORT=8080

CMD ["sh", "-c", "reflex start --env prod --port $PORT --loglevel debug"]
