FROM python:3.8.10-slim
ADD ./app /app
WORKDIR /app
RUN apt-get update \
    && apt-get install -y binutils \
    && pip install -r requirements.txt \
    && chmod -x /app/flag
RUN useradd ssti
USER ssti
CMD python3 app.py
