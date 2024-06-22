FROM python:3.11-alpine

WORKDIR /api
COPY . /api/

RUN pip install -r requirements.txt

CMD ["uvicorn", "mainApi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
