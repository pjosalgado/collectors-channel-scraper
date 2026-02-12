# -*- coding: utf-8 -*-

import logging as log
import requests
from scrapy.exceptions import DropItem
import time

class TelegramPipeline(object):

    def __init__(self, token, chat_id, thread_id, parse_mode, discount_percentage, restock_notification):
        self.token = token
        self.chat_id = chat_id
        self.thread_id = thread_id
        self.parse_mode = parse_mode
        self.discount_percentage = discount_percentage
        self.restock_notification = restock_notification

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            token = crawler.settings.get('TELEGRAM_TOKEN'), 
            chat_id = crawler.settings.get('TELEGRAM_CHAT_ID'), 
            thread_id = crawler.settings.get('TELEGRAM_THREAD_ID'), 
            parse_mode = crawler.settings.get('TELEGRAM_PARSE_MODE'),
            discount_percentage = float(crawler.settings.get('NOTIFICATION_DISCOUNT_PERCENTAGE')),
            restock_notification = crawler.settings.get('NOTIFICATION_RESTOCK') == "True"
        )


    def process_item(self, item, spider):

        log.debug('Processing in TelegramPipeline item <{}>'.format(item))

        if 'previous_price' in item:
            message_text = get_notification_status(self, item)
        else:
            message_text = '🆕 Novo no catálogo'

        price = item['price'].replace('.', ',')

        if message_text is None or price == 'Indisponível':
            log.debug('Not sending Telegram notification for item <{}>'.format(item.get('url')))
            return item

        title = item['title']
        title_type = item['title_type']
        spider_pretty_name = item['spider_pretty_name']
        url = item['url']
        cover_url = item['cover_url']

        message = '*{}*'.format(title)
        message += '\n📀 {}'.format(title_type) if title_type != None else ''
        message += '\n💵 {} - R$ {}'.format(spider_pretty_name, price)
        message += '\n{}'.format(message_text)
        message += '\n🔗 {}'.format(url)
        message += '\n\n📄 _{}_'.format(item['spider_url_pretty_name'])

        if 'additional_info' in item:
            message += '\n⚠️ _{}_'.format(item['additional_info'])

        url = 'https://api.telegram.org/bot' + self.token + '/sendPhoto'
        data = {
            'chat_id': self.chat_id, 
            'message_thread_id': self.thread_id, 
            'photo': cover_url, 
            'parse_mode': self.parse_mode, 
            'caption': message
        }

        log.info('Sending Telegram notification for item <{}>'.format(item.get('url')))
        requests.post(url, data)

        time.sleep(0.5) # prevent rate limit

        return item


def get_notification_status(self, item):

    new_price_value = item['price']
    old_price_value = item['previous_price']

    try:
        if float(new_price_value) < float(old_price_value):
            old_price = float(old_price_value)
            new_price = float(new_price_value)
            percentage_difference = round(((old_price - new_price) / old_price) * 100)

            if percentage_difference >= self.discount_percentage:
                old_price_value = old_price_value.replace('.', ',')
                return '⬇️ {}% - Custava R$ {}'.format(percentage_difference, old_price_value)
    except:
        if old_price_value == 'Indisponível' and new_price_value != 'Indisponível' and self.restock_notification: 
            return '🔄 Estava indisponível'

    return None
