#
# Tesseract 4 OCR Runtime Environment - Docker Container
#

FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-eng 

RUN mkdir /home/work
WORKDIR /home/work

COPY parse.sh /home/work
RUN chmod +x /home/work/parse.sh

CMD ["/home/work/parse.sh", "/var/data"]