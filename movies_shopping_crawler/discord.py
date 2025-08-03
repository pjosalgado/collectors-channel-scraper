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

        if 'old_item' in item: 
            notification_type = get_notification_status(self, item['old_item'], item)
        else: 
            notification_type = ':new: Novo no catálogo'
    
        price = item['price'].replace('.', ',')

        if notification_type is None or price == 'Indisponível': 
           raise DropItem('Status not relevant in item <{}>'.format(item))

        if 'additional_info' in item:
            additional_info = '⚠️ {}'.format(item['additional_info'])
        else:
            additional_info = ''

        json = {
            'embeds': [{
                'title': item['title'],
                'url': item['url'],
                'color': item['color_theme_decimal'],
                'thumbnail': {
                    'url': item['cover_url']
                },
                'fields': [
                    {
                        'name': 'Status',
                        'value': notification_type,
                        'inline': False
                    },
                    {
                        'name': 'Tipo',
                        'value': item['title_type'],
                        'inline': False
                    },
                    {
                        'name': 'Preço',
                        'value': 'R$ {}'.format(price),
                        'inline': True
                    },
                    {
                        'name': 'Loja',
                        'value': item['spider_pretty_name'],
                        'inline': True
                    }
                ],
                'footer': {
                    'text': additional_info
                },
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
                return ':arrow_down: {}% - antes custava R$ {}'.format(percentage_difference, old_price_value)
    except: 
        if old_price_value == 'Indisponível' and new_price_value != 'Indisponível' and self.restock_notification: 
            return ':arrows_counterclockwise: Antes estava indisponível'

    return None
