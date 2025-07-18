# -*- coding: utf-8 -*-

import logging as log
import requests
from scrapy.exceptions import DropItem

class DiscordPipeline(object): 

    def __init__(self, url, discount_percentage, restock_notification): 
        self.url = url
        self.discount_percentage = discount_percentage
        self.restock_notification = restock_notification

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            url = crawler.settings.get('DISCORD_URL'),
            discount_percentage = float(crawler.settings.get('NOTIFICATION_DISCOUNT_PERCENTAGE')),
            restock_notification = crawler.settings.get('NOTIFICATION_RESTOCK') == "True"
        )


    def process_item(self, item, spider): 

        log.info('Processing in DiscordPipeline item <{}>'.format(item))

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

        message = '**{}**'.format(title)
        message += '\n:dvd: {}'.format(title_type) if title_type != None else ''
        message += '\n:dollar: R$ {} - {}'.format(price, spider_pretty_name)
        message += '\n{}'.format(notification)
        message += '\n:link: {}'.format(url)

        if 'additional_info' in item:
            additional_info = item['additional_info']
            message += '\n:warning: {}'.format(additional_info)

        json = {
            'content': message,
            'embeds': [{
                'image': {
                    'url': cover_url
                }
            }]
        }

        headers = {
            'Content-Disposition': 'form-data',
            'Content-Type': 'application/json'
        }

        log.info('Sending message to Discord...')
        requests.post(self.url, json=json, headers=headers)

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
                return ':arrow_down: {}% - antes era R$ {}'.format(percentage_difference, old_price_value)
    except: 
        if old_price_value == 'Indisponível' and new_price_value != 'Indisponível' and self.restock_notification: 
            return ':arrows_counterclockwise: antes estava indisponível'

    return None
