#!/bin/bash

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🏃 Starting spiders'

args="-a PAGINATION_ENABLED=$PAGINATION_ENABLED"

mongo_settings="-s MONGO_URL=$MONGO_URL"
influxdb_settings="-s INFLUXDB_URL=$INFLUXDB_URL -s INFLUXDB_ORG=$INFLUXDB_ORG -s INFLUXDB_TOKEN=$INFLUXDB_TOKEN -s INFLUXDB_BUCKET=$INFLUXDB_BUCKET"
discord_settings="-s DISCORD_URL=$DISCORD_URL"
telegram_settings="-s TELEGRAM_TOKEN=$TELEGRAM_TOKEN -s TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID"
notification_settings="-s NOTIFICATION_DISCOUNT_PERCENTAGE=$NOTIFICATION_DISCOUNT_PERCENTAGE -s NOTIFICATION_RESTOCK=$NOTIFICATION_RESTOCK"
additional_settings="-s AUTOUNIT_ENABLED=False"
settings="${mongo_settings} ${influxdb_settings} ${discord_settings} ${telegram_settings} ${notification_settings} ${additional_settings}"

rm -r -f autounit
mkdir -p logs
mkdir -p outputs

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 Amazon'
scrapy crawl amazon ${args} ${settings} -o outputs/amazon-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/amazon-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 Colecione Clássicos'
scrapy crawl colecioneclassicos ${args} ${settings} -o outputs/colecioneclassicos-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/colecioneclassicos-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 Fam DVD'
scrapy crawl famdvd ${args} ${settings} -o outputs/famdvd-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/famdvd-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 iMusic BR'
scrapy crawl imusicbr ${args} ${settings} -o outputs/imusicbr-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/imusicbr-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 The Originals'
scrapy crawl theoriginals ${args} ${settings} -o outputs/theoriginals-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/theoriginals-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- 🔍 Versátil'
scrapy crawl versatil ${args} ${settings} -o outputs/versatil-$(date +'%Y-%m-%d-%H-%M-%S').csv # &> logs/versatil-$(date +'%Y-%m-%d-%H-%M-%S').log

echo $(date +'%d/%m/%Y %H:%M:%S') '- ✅ Process finished!'
exit 0
