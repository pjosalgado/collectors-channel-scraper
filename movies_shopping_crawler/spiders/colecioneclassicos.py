# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class ColecioneClassicosSpider(scrapy.Spider):

    name               = 'colecioneclassicos'
    spider_pretty_name = 'Colecione Clássicos'

    urls = {
        'Box e Coleções'
            : 'https://www.colecioneclassicos.com.br/box-e-colecoes',

        'Destaques Imperdíveis'
            : 'https://www.colecioneclassicos.com.br/de-volta-a-loja',

        'Obras-Primas do Cinema'
            : 'https://www.colecioneclassicos.com.br/OP',

        'Pré-Venda'
            : 'https://www.colecioneclassicos.com.br/pre-venda',

        'Lançamentos'
            : 'https://www.colecioneclassicos.com.br/lancamentos',

        'Busca "4K"'
            : 'https://www.colecioneclassicos.com.br/buscar?q=4K',
    }

    start_urls = list(urls.values())

    ignored_categories = [
    ]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        try:
            pagination_enabled = kwargs['PAGINATION_ENABLED'] == "True"
        except:
            pagination_enabled = False

        try:
            max_pages = int(kwargs['PAGINATION_LIMIT'])
        except:
            max_pages = None

        spider = cls(*args, pagination_enabled=pagination_enabled, max_pages=max_pages, **kwargs)
        spider._set_crawler(crawler)

        return spider


    async def start(self):
        for name, url in self.urls.items():
            response = self.fetch_page(url, name)
            for item in self.parse(response):
                yield item


    def parse(self, response):

        log.info('Visited <{}> - HTTP status: {}'.format(response.url, response.status))

        spider_url_pretty_name = response.meta.get('spider_url_pretty_name', response.url)
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
        current_page = response.meta.get('current_page', 1)

        result = response.css('.listagem-item')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = movie_selector.css('.nome-produto::text').get().strip()
            title = full_title
            title_type = self.get_title_type(full_title)

            url = movie_selector.css('.produto-sobrepor::attr(href)').get().strip()
            
            price = movie_selector.css('.preco-promocional::text').get()
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível':
                price = price.replace(' ', '').replace('R$', '').replace(',', '.')
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
            if self.max_pages is None or current_page < self.max_pages:
                next_page = response.css('a[rel=next]::attr(href)').get()
                if next_page and next_page != '#':
                    next_page = response.urljoin(next_page.strip())
                    log.info('Next page is <{}>'.format(next_page))
                    response = self.fetch_page(next_page, spider_url_pretty_name, current_page + 1)
                    yield from self.parse(response)
                else:
                    log.info('Next page not found')
            else:
                log.info('Max pages reached: {}'.format(self.max_pages))
        else:
            log.info('Pagination is disabled')


    def get_title_type(self, full_title, default_type = 'DVD'):
        full_title = full_title.lower().replace('-', '').replace(' ', '')
        if 'bluray' in full_title or 'bd' in full_title:
            return 'Blu-ray'
        else:
            return default_type


    def fetch_page(self, url, spider_url_pretty_name, current_page=1):

        request = Request(
            url=url,
            meta={
                'spider_url_pretty_name': spider_url_pretty_name,
                'current_page': current_page,
            }
        )
        request_body = requests.get(url, impersonate="chrome")
        response = HtmlResponse(url=url, body=request_body.text, encoding="utf-8", request=request)

        time.sleep(self.settings.getfloat('DOWNLOAD_DELAY', 2))

        return response
