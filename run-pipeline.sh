#!/bin/bash
docker run --rm -v sacorona_data_volume:/var/data sacorona/scrapy:latest \
&& \
docker run --rm -v sacorona_data_volume:/var/data sacorona/tesseract:latest \
&& \
docker run --rm -v sacorona_data_volume:/var/data sacorona/text-clean:latest \
&& \
docker run --rm -v sacorona_data_volume:/var/data sacorona/text-process:latest 