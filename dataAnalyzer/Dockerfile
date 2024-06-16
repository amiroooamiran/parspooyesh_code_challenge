FROM python:3.11-alpine

WORKDIR /analyzer
COPY . /analyzer/

RUN pip install -r requirements.txt

CMD ["python", "./reciver.py"]