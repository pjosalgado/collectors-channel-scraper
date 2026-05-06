# -*- coding: utf-8 -*-

import logging as log
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDbPipeline(object):

    def __init__(self, url, org, token, bucket, spider):
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket
        self.spider = spider


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url = crawler.settings.get('INFLUXDB_URL'),
            org = crawler.settings.get('INFLUXDB_ORG'),
            token = crawler.settings.get('INFLUXDB_TOKEN'),
            bucket = crawler.settings.get('INFLUXDB_BUCKET'),
            spider = crawler.spider
        )


    def open_spider(self):
        self.client = InfluxDBClient(url=self.url, token=self.token)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        log.debug('Opened InfluxDB connection to <{}>'.format(self.spider.name))
        self.data = []


    def close_spider(self):
        if self.client and self.write_api:
            log.debug('Writing on InfluxDB these points <{}>'.format(self.data))
            self.write_api.write(self.bucket, self.org, self.data)
            self.write_api.close()
            self.client.close()
            log.debug('Closed InfluxDB connection to <{}>'.format(self.spider.name))
        else:
            log.debug('InfluxDB connection already closed to <{}>'.format(self.spider.name))


    def process_item(self, item):

        log.debug('Processing in InfluxDbPipeline item <{}>'.format(item))

        spider_name = item['spider']
        measurement = 'prices_{}'.format(spider_name)

        title = item['title']
        title_type = item['title_type']
        timestamp = item['timestamp']
        price = item['price']

        if price != 'Indisponível':
            self.data.append({
                'measurement': measurement,
                'tags': {
                    'title': title,
                    'title_type': title_type
                },
                'time': timestamp,
                'fields': {
                    'price': float(price)
                }
            })

        return item
