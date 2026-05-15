# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
import re
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class FilmiccaSpider(scrapy.Spider):

    name               = 'filmicca'
    spider_pretty_name = 'FILMICCA'

    urls = {
        'Blu-rays'
            : 'https://loja.filmicca.com.br/collections/blu-rays',
    }

    start_urls = list(urls.values())

    ignored_categories = [
    ]


    async def start(self):
        for name, url in self.urls.items():
            response = self.fetch_page(url, name)
            for item in self.parse(response):
                yield item


    def parse(self, response):

        log.info('Visited <{}> - HTTP status: {}'.format(response.url, response.status))

        spider_url_pretty_name = response.meta.get('spider_url_pretty_name', response.url)
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        result = response.css('.card')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = movie_selector.css('h3 > a::text').get().strip()
            title, title_type = self.get_title_details(full_title)

            url = movie_selector.css('h3 > a::attr(href)').get().strip()
            url = 'https://loja.filmicca.com.br' + url

            price = movie_selector.css('.price-item--last::text').get().strip()
            price = price.replace(' ', '').replace('R$', '').replace(',', '.')
            price = '%.2f' % float(price)

            cover_url = movie_selector.css('.card__media > div > img::attr(src)').get().strip()
            cover_url = 'http:' + cover_url

            if title_type not in self.ignored_categories:
                title_found = {
                    'spider': self.name,
                    'spider_pretty_name': self.spider_pretty_name,
                    'spider_url': response.url,
                    'spider_url_pretty_name': spider_url_pretty_name,
                    'timestamp': timestamp,
                    'full_title': full_title,
                    'title': title,
                    'title_type': title_type,
                    'url': url,
                    'price': price,
                    'cover_url': cover_url
                }
                log.debug('Title found: {}'.format(full_title))
                yield title_found
            else:
                log.debug('Ignoring title due to filter: {}'.format(full_title))

        log.info('Pagination is disabled')


    def get_title_details(self, full_title, default_type = 'Blu-ray'):
        cleaned_title = re.sub(r'\s*\([^)]*\)\s*', '', full_title).strip()
        cleaned_title = cleaned_title.replace('Pré-venda: ', '')
        if 'blu-ray' in full_title.lower():
            return (cleaned_title, 'Blu-ray')
        else:
            return (cleaned_title, default_type)


    def fetch_page(self, url, spider_url_pretty_name):

        request = Request(
            url=url,
            meta={
                'spider_url_pretty_name': spider_url_pretty_name
            }
        )
        request_body = requests.get(url, impersonate="chrome")
        response = HtmlResponse(url=url, body=request_body.text, encoding="utf-8", request=request)

        time.sleep(2)

        return response
