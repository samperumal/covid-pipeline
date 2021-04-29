FROM python:3.8-slim

RUN pip install psycopg2-binary

COPY ./src/ /opt/

WORKDIR /opt
CMD ["python", "main.py"]
