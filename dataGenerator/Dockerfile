FROM python:3.11-alpine
WORKDIR /generator
COPY . /generator/

RUN pip install -r requirements.txt

CMD ["python", "./datas.py"]
