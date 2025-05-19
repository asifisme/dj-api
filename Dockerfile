FROM python:3.13-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk add --no-cache --virtual .build-deps \
    gcc musl-dev libffi-dev jpeg-dev zlib-dev python3-dev build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

FROM python:3.13-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

EXPOSE 8080

CMD ["gunicorn", "xApi.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
