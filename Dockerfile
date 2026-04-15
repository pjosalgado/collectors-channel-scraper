FROM python:3.12.7-slim

LABEL MAINTAINER="Paulo Salgado <pjosalgado@gmail.com>"
LABEL VERSION="$VERSION"

WORKDIR /python-docker

RUN apt update && apt install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root --only main

COPY scrapy.cfg .
COPY movies_shopping_crawler movies_shopping_crawler
COPY scripts/run-all-spiders.sh .

CMD ["./run-all-spiders.sh"]
