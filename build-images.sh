#!/bin/bash
docker build -t sacorona/scrapy scrapy/
docker build -t sacorona/tesseract tesseract-ocr-re/
docker build -t sacorona/text-clean text-clean/
docker build -t sacorona/text-process text-process/
docker build -t sacorona/azure-blob azure-blob/
