FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD ["sh", "-c", "reflex start --env prod --host 0.0.0.0 --port $PORT --loglevel debug"]