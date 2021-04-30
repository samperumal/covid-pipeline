FROM python:3.8-slim

RUN python -m pip install pip --upgrade

COPY requirements.txt /opt
RUN pip install -r /opt/requirements.txt

COPY ./src/ /opt/

WORKDIR /opt
ENTRYPOINT ["python"]
