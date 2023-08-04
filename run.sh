#!/bin/bash

args='-a PAGINATION_ENABLED=False'

mongo_settings="-s MONGO_URL=$MONGO_URL"
influxdb_settings="-s INFLUXDB_URL=$INFLUXDB_URL -s INFLUXDB_ORG=$INFLUXDB_ORG -s INFLUXDB_TOKEN=$INFLUXDB_TOKEN -s INFLUXDB_BUCKET=$INFLUXDB_BUCKET"
discord_settings="-s DISCORD_URL=$DISCORD_URL"
# telegram_settings="-s TELEGRAM_TOKEN=$TELEGRAM_TOKEN -s TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID"
settings="-s AUTOUNIT_ENABLED=False ${mongo_settings} ${influxdb_settings} ${discord_settings}"

mkdir -p logs
rm -r -f autounit

# echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Amazon...'
# scrapy crawl amazon ${args} ${settings} -o outs/amazon-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/amazon-$(date +'%Y-%m-%d-%H-%M-%S').log

# echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Colecione Clássicos...'
# scrapy crawl colecioneclassicos ${args} ${settings} -o outs/colecioneclassicos-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/colecioneclassicos-$(date +'%Y-%m-%d-%H-%M-%S').log

# echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Fam DVD...'
# scrapy crawl famdvd ${args} ${settings} -o outs/famdvd-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/famdvd-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping The Originals...'
scrapy crawl theoriginals ${args} ${settings} -o outs/theoriginals-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/theoriginals-$(date +'%Y-%m-%d-%H-%M-%S').log

# echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Vídeo Pérola...'
# scrapy crawl videoperola ${args} ${settings} -o outs/videoperola-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/videoperola-$(date +'%Y-%m-%d-%H-%M-%S').log
