FROM python:3.9-alpine

WORKDIR /app/parser

COPY ./requirements.txt /app/parser/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]