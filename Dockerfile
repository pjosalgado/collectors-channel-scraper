FROM python:3.12.7-slim

LABEL MAINTAINER="Paulo Salgado <pjosalgado@gmail.com>"

WORKDIR /python-docker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

COPY scrapy.cfg .
COPY movies_shopping_crawler movies_shopping_crawler
COPY scripts/run-all-spiders.sh .

LABEL VERSION="$VERSION"

CMD ["./run-all-spiders.sh"]
