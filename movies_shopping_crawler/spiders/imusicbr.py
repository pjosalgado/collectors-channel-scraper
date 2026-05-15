# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import time
import pytz
from curl_cffi import requests
from scrapy.http import HtmlResponse
import scrapy
from scrapy import Request
from tomlkit import item
import logging as log

class ImusicBrSpider(scrapy.Spider):

    name               = 'imusicbr'
    spider_pretty_name = 'iMusic BR'

    urls = {
        '4K UHD & Blu-ray Steelbooks'
            : 'https://imusic.br.com/exposure/18451/4k-uhd-blu-ray-steelbooks',

        'Filmes da coleção Criterion'
            : 'https://imusic.br.com/exposure/18490/filmes-da-colecao-criterion',

        'Filme 4K UHD'
            : 'https://imusic.br.com/exposure/13562/filme-4k-uhd',

        'Filmes e séries novos e futuros'
            : 'https://imusic.br.com/exposure/29/filmes-e-series-novos-e-futuros',

        'DVD e Blu-ray - Mais Vendido'
            : 'https://imusic.br.com/exposure/11084/dvd-e-blu-ray-mais-vendido',

        'Crunchyroll'
            : 'https://imusic.br.com/exposure/22810/crunchyroll',
    }

    ignored_categories = [
        'Paperback Book',
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

        result = response.css('.item-teaser')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            title = movie_selector.css('.title::attr(title)').get().strip()
            title_type = movie_selector.css('.type > span > acronym::text').get().strip()
            full_title = title_type + ' - ' + title

            url = movie_selector.css('a::attr(href)').get().strip()
            url = 'https://imusic.br.com' + url

            price = movie_selector.css('.price::text').get()
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível':
                price = price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.').strip()
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('.item-cover::attr(src)').get().strip()

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
                    'cover_url': cover_url,
                    'additional_info': '+ ~95% de impostos'
                }
                log.debug('Title found: {}'.format(full_title))
                yield title_found
            else:
                log.debug('Ignoring title due to filter: {}'.format(full_title))

        if self.pagination_enabled:
            next_page = response.css('.navbar-right > .btn-primary')
            next_page = next_page[1].css('::attr(href)').get() if len(next_page) > 0 else None
            if next_page:
                next_page = response.urljoin(next_page.strip())
                log.info('Next page is <{}>'.format(next_page))
                response = self.fetch_page(next_page, spider_url_pretty_name)
                yield from self.parse(response)
            else:
                log.info('Next page not found')
        else:
            log.info('Pagination is disabled')


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
