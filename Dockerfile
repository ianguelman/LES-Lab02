FROM python:3.11.0a5-alpine3.15

WORKDIR /home/python/lab01

COPY . ./

RUN pip install -r requirements.txt

CMD python index.py