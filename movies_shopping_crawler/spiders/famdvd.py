# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class FamDvdSpider(scrapy.Spider):

    name               = 'famdvd'
    spider_pretty_name = 'Fam DVD'

    urls = {
        'Exclusivos'
            : 'https://www.famdvd.com.br/exclusivos-1.html',

        'Lançamentos'
            : 'https://www.famdvd.com.br/lancamento.html',

        'Pré-venda'
            : 'https://www.famdvd.com.br/pre-venda.html',

        'Busca "4K"'
            : 'https://www.famdvd.com.br/catalogsearch/result/?q=4K',
    }

    start_urls = list(urls.values())

    ignored_categories = [
        'Funko Pop!',
    ]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        try:
            pagination_enabled = kwargs['PAGINATION_ENABLED'] == "True"
        except:
            pagination_enabled = False

        spider = cls(*args, pagination_enabled=pagination_enabled, **kwargs)
        spider._set_crawler(crawler)

        return spider


    async def start(self):
        for name, url in self.urls.items():
            response = self.fetch_page(url, name)
            for item in self.parse(response):
                yield item


    def parse(self, response):

        log.info('Visited <{}>'.format(response.url))

        spider_url_pretty_name = response.meta.get('spider_url_pretty_name', response.url)
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        result = response.css('.products-grid > li.item')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = movie_selector.css('h3 > a::text').get().strip()
            title, title_type = self.get_title_details(full_title)

            url = movie_selector.css('h3 > a::attr(href)').get().strip()
            
            price = movie_selector.css('.special-price > .price::text').get()
            price = movie_selector.css('.price::text').get() if price is None else price
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível':
                price = price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('img::attr(src)').get().strip()

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

        if self.pagination_enabled:
            next_page = response.css('.i-next::attr(href)').get()
            if next_page:
                next_page = response.urljoin(next_page.strip())
                log.info('Next page is <{}>'.format(next_page))
                response = self.fetch_page(next_page, spider_url_pretty_name)
                yield from self.parse(response)
            else:
                log.info('Next page not found')
        else:
            log.info('Pagination is disabled')


    def get_title_details(self, full_title, default_type = 'DVD'):
        if full_title.lower().startswith('blu-ray'):
            title_split = full_title.split(' - ', 1)
            return (title_split[1].strip(), title_split[0].strip())
        if full_title.lower().startswith('funko pop!'):
            title_split = full_title.split(' - ', 1)
            return (title_split[1].strip(), 'Funko Pop!')
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
