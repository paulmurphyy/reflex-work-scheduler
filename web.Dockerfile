FROM python:3.12 AS builder

WORKDIR /app

COPY . .
ENV API_URL=http://ec2-XX-XXX-XXX-XX.us-west-2.compute.amazonaws.com
RUN pip install -r requirements.txt
RUN reflex export --frontend-only --no-zip


COPY --from=builder /app/.web/build/client ./docs/
