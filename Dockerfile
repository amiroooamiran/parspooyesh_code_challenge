FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /weatherProject
COPY requirements.txt /weatherProject/

RUN pip install -r requirements.txt

COPY . /weatherProject/
