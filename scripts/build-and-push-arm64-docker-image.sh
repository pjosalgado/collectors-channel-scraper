#!/bin/bash
docker buildx build --platform=linux/arm64 --push -t paulosalgado/collectors-channel-scraper:2.7.0 .
