#!/bin/bash

args='-a PAGINATION_ENABLED=False'
settings='-s ITEM_PIPELINES={}'

mkdir -p logs
rm -r -f autounit

echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Amazon...'
touch logs/amazon.log
scrapy crawl amazon ${args} ${settings} -o outs/amazon-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/amazon.log

echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Fam DVD...'
touch logs/famdvd.log
scrapy crawl famdvd ${args} ${settings} -o outs/famdvd-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/famdvd.log

echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping The Originals...'
touch logs/theoriginals.log
scrapy crawl theoriginals ${args} ${settings} -o outs/theoriginals-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/theoriginals.log

echo $(date +'%d/%m/%Y %H:%M:%S') '- scraping Vídeo Pérola...'
touch logs/videoperola.log
scrapy crawl videoperola ${args} ${settings} -o outs/videoperola-$(date +'%Y-%m-%d-%H-%M-%S').csv &>logs/videoperola.log
