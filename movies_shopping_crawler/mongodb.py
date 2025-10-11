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
        log.info('Opened MongoDB connection to <{}>'.format(spider.name))


    def close_spider(self, spider):
        if self.client:
            self.client.close()
            log.info('Closed MongoDB connection to <{}>'.format(spider.name))
        else:
            log.info('MongoDB connection already closed to <{}>'.format(spider.name))


    def process_item(self, item, spider):

        log.info('Processing in MongoDbPipeline item <{}>'.format(item))

        item_found = self.col.find_one({'url': item['url']})

        if item_found:
            id_item_found = item_found.get('_id')
            item.update({'_id': id_item_found})
            item.update({'created_at': item_found.get('created_at')})
            self.col.update_one({'_id': id_item_found}, {'$set': dict(item)})
            log.info('Updated item with id <{}> using <{}>'.format(id_item_found, item))
            item.update({'old_item': item_found})
        else:
            created_at = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
            item.update({'created_at': created_at})
            id_item_new = self.col.insert_one(dict(item)).inserted_id
            item.update({'_id': id_item_new})
            log.info('Inserted item <{}> with id <{}>'.format(item, id_item_new))

        return item
