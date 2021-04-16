FROM python:3.8-slim

COPY requirements.txt /opt/scrapy/requirements.txt

RUN pip install -r /opt/scrapy/requirements.txt

COPY sacoronavirus/ /opt/scrapy/sacoronavirus/

WORKDIR /opt/scrapy/sacoronavirus

CMD ["scrapy", "crawl", "updates"]
