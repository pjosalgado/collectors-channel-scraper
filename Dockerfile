FROM python:3.12.7-slim

LABEL MAINTAINER="Paulo Salgado <pjosalgado@gmail.com>"

WORKDIR /python-docker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update && apt-get install -y \
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

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

RUN playwright install chromium

COPY scrapy.cfg .
COPY movies_shopping_crawler movies_shopping_crawler
COPY scripts/run-all-spiders.sh .

LABEL VERSION="$VERSION"

CMD ["./run-all-spiders.sh"]
