FROM python:3.12.7-slim

LABEL MAINTAINER="Paulo Salgado <pjosalgado@gmail.com>"
LABEL VERSION="$VERSION"

WORKDIR /python-docker

RUN apt update && apt install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root --only main

RUN playwright install chromium

COPY scrapy.cfg .
COPY movies_shopping_crawler movies_shopping_crawler
COPY scripts/run-all-spiders.sh .

CMD ["./run-all-spiders.sh"]
