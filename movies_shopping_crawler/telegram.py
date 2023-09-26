# -*- coding: utf-8 -*-

import logging as log
import requests
from scrapy.exceptions import DropItem

class TelegramPipeline(object): 

    def __init__(self, token, chat_id, parse_mode, discount_percentage): 
        self.token = token
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.discount_percentage = discount_percentage

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            token = crawler.settings.get('TELEGRAM_TOKEN'), 
            chat_id = crawler.settings.get('TELEGRAM_CHAT_ID'), 
            parse_mode = crawler.settings.get('TELEGRAM_PARSE_MODE'),
            discount_percentage = float(crawler.settings.get('NOTIFICATION_DISCOUNT_PERCENTAGE'))
        )

    def process_item(self, item, spider): 

        log.info('Processing in TelegramPipeline item <{}>'.format(item))

        price = item['price']

        if 'old_item' in item: 
            notification = get_notification_status(self, item['old_item'], item)
        else: 
            notification = '🆕'
    
        if notification is None or price == 'Indisponível': 
            raise DropItem('Status not relevant in item <{}>'.format(item))

        title = item['title']
        title_type = item['title_type']
        spider_pretty_name = item['spider_pretty_name']
        url = item['url']
        cover_url = item['cover_url']
        price = price.replace('.', ',')

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

        log.info('Sending message to Telegram...')
        requests.post(url, data)

        return item


def get_notification_status(self, old, new): 

    old_price_value = old['price']
    new_price_value = new['price']

    try: 
        if float(new_price_value) < float(old_price_value): 
            old_price = float(old_price_value)
            new_price = float(new_price_value)
            percentage_difference = round(((old_price - new_price) / old_price) * 100)

            if percentage_difference >= self.discount_percentage: 
                old_price_value = old_price_value.replace('.', ',')
                return '⬇️ {}% - antes era R$ {}'.format(percentage_difference, old_price_value)
    except: 
        if old_price_value == 'Indisponível' and new_price_value != 'Indisponível': 
            return '🔄 antes estava indisponível'
        elif new_price_value != old_price_value: 
            old_price_value = old_price_value.replace('.', ',')
            return '🔄 antes era R$ {}'.format(old_price_value)

    return None
