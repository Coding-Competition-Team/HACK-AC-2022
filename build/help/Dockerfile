FROM python:3.10

ENV BOT_TOKEN=MTAxMTQxODM1MzY2NTA2OTA5Ng.GIh25B.QG8pfqhqI1WIFCy9wquFceuXBXWViIrf80VQq0
COPY . /app
WORKDIR /app

RUN python3 -m pip install -r /app/requirements.txt

CMD ["python3", "main.py"]
