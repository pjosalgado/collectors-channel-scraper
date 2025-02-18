FROM python:3.13.2-slim

LABEL maintainer="Paulo Salgado <pjosalgado@gmail.com>"
LABEL version="2.6.1"

WORKDIR /python-docker

RUN apt update \
    && apt install -y curl

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY scrapy.cfg .
COPY movies_shopping_crawler movies_shopping_crawler
COPY scripts/run-all-spiders.sh .

CMD [ "./run-all-spiders.sh" ]
