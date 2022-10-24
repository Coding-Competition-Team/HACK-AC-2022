FROM python:3.8.10-slim
ENV WERKZEUG_DEBUG_PIN=113-218-154
ADD . /app
WORKDIR /app
RUN apt update \
    && apt install -y firefox-esr \
    && pip install -r requirements.txt
RUN chmod +x geckodriver
CMD flask --debug run --host 0.0.0.0 -p 5000
