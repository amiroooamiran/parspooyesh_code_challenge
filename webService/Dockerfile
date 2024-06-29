FROM python:3.11-alpine

WORKDIR /webservice
COPY . /webservice/

RUN pip install -r requirements.txt

CMD ["uvicorn", "mainApi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
