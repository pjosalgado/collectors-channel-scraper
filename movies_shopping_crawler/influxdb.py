# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging as log
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDbPipeline(object): 

    def __init__(self, url, org, token, bucket): 
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            url = crawler.settings.get('INFLUXDB_URL'), 
            org = crawler.settings.get('INFLUXDB_ORG'), 
            token = crawler.settings.get('INFLUXDB_TOKEN'), 
            bucket = crawler.settings.get('INFLUXDB_BUCKET')
        )

    def open_spider(self, spider): 
        self.client = InfluxDBClient(url=self.url, token=self.token)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        log.info('Opened InfluxDB connection to <{}>'.format(spider.name))
        self.data = []

    def close_spider(self, spider): 
        if self.client and self.write_api: 
            log.info('Writing on InfluxDB these points <{}>'.format(self.data))
            self.write_api.write(self.bucket, self.org, self.data)
            self.write_api.close()
            self.client.close()
            log.info('Closed InfluxDB connection to <{}>'.format(spider.name))
        else: 
            log.info('InfluxDB connection already closed to <{}>'.format(spider.name))

    def process_item(self, item, spider):

        log.info('Processing in InfluxDbPipeline item <{}>'.format(item))

        spider_name = item['spider']
        measurement = 'prices_{}'.format(spider_name)

        title = item['title']
        title_type = item['title_type']
        timestamp = item['timestamp']
        price = item['price']

        self.data.append({
            'measurement': measurement,
            'tags': {
                'title': title, 
                'title_type': title_type
            },
            'time': timestamp,
            'fields': {
                'price': price
            }
        })

        return item
