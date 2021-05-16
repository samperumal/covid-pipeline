FROM python:3.8-slim

COPY requirements.txt /opt/requirements.txt

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install -r /opt/requirements.txt

COPY sacoronavirus/ /opt/sacoronavirus/

WORKDIR /opt/sacoronavirus

CMD ["scrapy", "crawl", "updates"]
