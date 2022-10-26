FROM python:3.8.10-slim
ENV USERNAME=admin
ENV PASSWORD=eNkfeunrNgVCe9xR3Xv4HeVw5Kx2VBC7
ADD . /app
WORKDIR /app
RUN apt update \
    && apt install -y firefox-esr \
    && pip install -r requirements.txt
RUN chmod +x geckodriver
CMD python3 ./app.py
