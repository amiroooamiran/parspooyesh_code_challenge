# Use an official Python runtime as a parent image
FROM python:3.11-alpine
WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./datas.py"]
