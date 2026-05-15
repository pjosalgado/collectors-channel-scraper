# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class VersatilSpider(scrapy.Spider):

    name               = 'versatil'
    spider_pretty_name = 'Versátil Home Vídeo'

    urls = {
        'Raridades'
            : 'https://www.versatilhv.com.br/raridades/c',

        'Pré-venda'
            : 'https://www.versatilhv.com.br/pre-venda/c',

        'Lançamentos'
            : 'https://www.versatilhv.com.br/lancamentos/c',

        'Edições Especiais'
            : 'https://www.versatilhv.com.br/edicoes-especiais/c',
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

        log.info('Visited <{}>'.format(response.url))

        spider_url_pretty_name = response.meta.get('spider_url_pretty_name', response.url)
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        result = response.css('.product-in-card')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = movie_selector.css('h3 > span::text').get().strip()
            title, title_type = self.get_title_details(full_title)

            url = movie_selector.css('.dados > a::attr(href)').get().strip()
            url = 'https://www.versatilhv.com.br' + url

            price = movie_selector.css('meta[itemprop=price]::attr(content)').get()
            is_unavailable = movie_selector.css('.announcement').get()

            if is_unavailable is None:
                price = price.strip()
                price = '%.2f' % float(price)
            else:
                price = 'Indisponível'

            cover_url = movie_selector.css('.image > img::attr(data-src)').get().strip()
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


    def get_title_details(self, full_title, default_type = 'DVD'):
        if full_title.lower().startswith('blu-ray'):
            title_split = full_title.split(': ', 1)
            return (title_split[1].strip(), title_split[0].strip())
        else:
            return (full_title, default_type)


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
