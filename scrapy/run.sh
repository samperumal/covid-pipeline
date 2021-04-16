#!/bin/bash
cd /opt/airflow/scrapy
source lenv/bin/activate
cd sacoronavirus
scrapy crawl updates
