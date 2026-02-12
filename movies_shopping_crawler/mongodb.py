# -*- coding: utf-8 -*-

import logging as log
from pymongo import MongoClient
from datetime import datetime
import pytz

class MongoDbPipeline(object):

    def __init__(self, url):
        self.url = url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url = crawler.settings.get('MONGO_URL')
        )


    def open_spider(self, spider):
        self.client = MongoClient(self.url)
        db = self.client.movies
        self.col = db[spider.name]
        log.debug('Opened MongoDB connection to <{}>'.format(spider.name))


    def close_spider(self, spider):
        if self.client:
            self.client.close()
            log.debug('Closed MongoDB connection to <{}>'.format(spider.name))
        else:
            log.debug('MongoDB connection already closed to <{}>'.format(spider.name))


    def process_item(self, item, spider):

        log.debug('Processing in MongoDbPipeline item <{}>'.format(item))

        item_found = self.col.find_one({'url': item['url']})

        if item_found:
            id_item_found, item = prepare_existing_item(self, item, item_found)
            self.col.update_one({'_id': id_item_found}, {'$set': dict(item)})
            log.info('Updated in MongoDB item <{}>'.format(item.get('url')))
            item.update({'old_item': item_found})
        else:
            item = prepare_new_item(self, item)
            id_new_item = self.col.insert_one(dict(item)).inserted_id
            item.update({'_id': id_new_item})
            log.info('Inserted in MongoDB item <{}>'.format(item.get('url')))

        return item


def prepare_existing_item(self, new_item, current_item):

    item_id = current_item.get('_id')

    new_item.update({'_id': item_id})
    new_item.update({'created_at': current_item.get('created_at')})
    new_item.update({'previous_price': current_item.get('price')})

    return item_id, new_item


def prepare_new_item(self, new_item):
    new_item.update({'created_at': new_item.get('timestamp')})
    return new_item
