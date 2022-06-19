# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging as log
import requests
from scrapy.exceptions import DropItem

class TelegramPipeline(object): 

    def __init__(self, token, chat_id, parse_mode): 
        self.token = token
        self.chat_id = chat_id
        self.parse_mode = parse_mode

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            token = crawler.settings.get('TELEGRAM_TOKEN'), 
            chat_id = crawler.settings.get('TELEGRAM_CHAT_ID'), 
            parse_mode = crawler.settings.get('TELEGRAM_PARSE_MODE')
        )

    def process_item(self, item, spider): 

        log.info('Processing in TelegramPipeline item <{}>'.format(item))

        notification = item['notification']

        if notification is None: 
            raise DropItem('Status not relevant in new item <{}>'.format(item))
    
        title = item['title']
        title_type = item['title_type']
        spider_pretty_name = item['spider_pretty_name']
        url = item['url']
        cover_url = item['cover_url']

        price = item['price']
        price = price.replace('.', ',')

        # Emojis: https://emojipedia.org/

        message = '*{}*'.format(title)
        message += '\n📀 {}'.format(title_type) if title_type != None else ''
        message += '\n💵 {} - R$ {}'.format(spider_pretty_name, price)
        message += '\n{}'.format(notification)
        message += '\n🔗 {}'.format(url)

        url = 'https://api.telegram.org/bot' + self.token + '/sendPhoto'
        data = {
            'chat_id': self.chat_id, 
            'photo': cover_url, 
            'parse_mode': self.parse_mode, 
            'caption': message
        }

        log.info('Sending to Telegram the message <{}>'.format(data))
        requests.post(url, data)

        return item
