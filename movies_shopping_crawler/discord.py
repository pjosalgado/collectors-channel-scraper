# -*- coding: utf-8 -*-

import logging as log
import requests
from scrapy.exceptions import DropItem

class DiscordPipeline(object):

    green_color_decimal  = 65280
    yellow_color_decimal = 16776960
    white_color_decimal  = 16777215

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

        if 'previous_price' in item:
            message_color, message_text = get_notification_status(self, item)
        else:
            message_color = self.green_color_decimal
            message_text = ':new: Novo no catálogo'

        price = item['price'].replace('.', ',')

        if message_text is None or price == 'Indisponível':
            log.warning('Status not relevant in item <{}>'.format(item))
            return item

        footer_message = '📄 {}'.format(item['spider_url_pretty_name'])

        if 'additional_info' in item:
            footer_message += '\n⚠️ {}'.format(item['additional_info'])

        json = {
            'embeds': [{
                'title': item['title'],
                'url': item['url'],
                'color': message_color,
                'thumbnail': {
                    'url': item['cover_url']
                },
                'fields': [
                    {
                        'name': 'Status',
                        'value': message_text,
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
                    'text': footer_message
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
                return self.yellow_color_decimal, ':arrow_down: {}%\nCustava R$ {}'.format(percentage_difference, old_price_value)
    except:
        if old_price_value == 'Indisponível' and new_price_value != 'Indisponível' and self.restock_notification: 
            return self.white_color_decimal, ':arrows_counterclockwise: Estava indisponível'

    return None, None
