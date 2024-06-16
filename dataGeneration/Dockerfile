# Use an official Python runtime as a parent image
FROM python:3.11-alpine
WORKDIR /generation
COPY . /generation/

RUN pip install -r requirements.txt

CMD ["python", "./datas.py"]
