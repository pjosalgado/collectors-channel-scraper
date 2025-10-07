#!/bin/bash
docker run -d --name collectors-channel-scraper --env-file=.env paulosalgado/collectors-channel-scraper:2.9.0
