FROM python:3.11.0a5-alpine3.15

WORKDIR /home/python/lab02

COPY . ./

RUN apk add --update docker openrc

RUN rc-update add docker boot

RUN pip install -r requirements.txt

CMD python index.py