FROM python:3.10

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y socat

WORKDIR /app
COPY . .

CMD [ "socat", "tcp-listen:50000,fork,reuseaddr", "EXEC:'python3 /app/run.py'" ]
