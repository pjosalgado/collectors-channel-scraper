# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class TheOriginalsSpider(scrapy.Spider):

    name               = 'theoriginals'
    spider_pretty_name = 'The Originals'

    urls = {
        'PRÉ-VENDA'
            : 'https://www.theoriginals.com.br/filmes-pre-venda',

        'LANÇAMENTOS'
            : 'https://www.theoriginals.com.br/filmes-lancamentos',

        '4K UHD'
            : 'https://www.theoriginals.com.br/4k-uhd',

        'COLEÇÃO'
            : 'https://www.theoriginals.com.br/filmes-colecao',

        'EDIÇÕES IMPORTADAS'
            : 'https://www.theoriginals.com.br/edicoes-importadas',

        'EXCLUSIVOS ED ESPECIAIS'
            : 'https://www.theoriginals.com.br/exclusivos',

        'STEELBOOK'
            : 'https://www.theoriginals.com.br/steelbook',

        'LP VINIL'
            : 'https://www.theoriginals.com.br/lp-vinil',

        'PROMOÇÕES'
            : 'https://www.theoriginals.com.br/filmes-promocoes',
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

        spider = cls(*args, pagination_enabled=pagination_enabled, **kwargs)
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
            next_page = response.css('a[rel=next]::attr(href)').get()
            if next_page and next_page != '#':
                next_page = response.urljoin(next_page.strip())
                log.info('Next page is <{}>'.format(next_page))
                response = self.fetch_page(next_page, spider_url_pretty_name)
                yield from self.parse(response)
            else:
                log.info('Next page not found')
        else:
            log.info('Pagination is disabled')


    def get_title_type(self, full_title, default_type = 'Desconhecido'):
        full_title = full_title.lower().replace('-', '').replace(' ', '')
        if 'bluray' in full_title or 'steelbook' in full_title:
            return 'Blu-ray'
        elif 'dvd' in full_title:
            return 'DVD'
        else:
            return default_type


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
