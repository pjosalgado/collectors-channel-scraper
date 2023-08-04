# -*- coding: utf-8 -*-

import logging as log
import requests
from scrapy.exceptions import DropItem

class DiscordPipeline(object): 

    def __init__(self, url): 
        self.url = url

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            url = crawler.settings.get('DISCORD_URL')
        )

    def process_item(self, item, spider): 

        log.info('Processing in DiscordPipeline item <{}>'.format(item))

        price = item['price']

        if 'old_item' in item: 
            notification = get_notification_status(item['old_item'], item)
        else: 
            notification = '🆕'
    
        if notification is None or price == 'Indisponível': 
           raise DropItem('Status not relevant in item <{}>'.format(item))

        title = item['title']
        title_type = item['title_type']
        spider_pretty_name = item['spider_pretty_name']
        url = item['url']
        # cover_url = item['cover_url']
        price = price.replace('.', ',')

        message = '**{}**'.format(title)
        message += '\n:dvd: {}'.format(title_type) if title_type != None else ''
        message += '\n:dollar: {} - R$ {}'.format(spider_pretty_name, price)
        message += '\n{}'.format(notification)
        message += '\n:link: {}'.format(url)

        data = {
            'content': message
        }

        log.info('Sending message to Discord...')
        requests.post(self.url, data)

        return item


def get_notification_status(old, new): 

    old_price = old['price']
    new_price = new['price']

    try: 
        if float(new_price) < float(old_price): 
            old_price = old_price.replace('.', ',')
            return ':arrow_down: antes era R$ {}'.format(old_price)
        else: 
            return None
    except: 
        if old_price == 'Indisponível': 
            return ':arrows_counterclockwise: antes estava indisponível'
        elif new_price != old_price: 
            old_price = old_price.replace('.', ',')
            return ':arrows_counterclockwise: antes era R$ {}'.format(old_price)
        else: 
            return None
