# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from curl_cffi import requests

class AmazonSpider(scrapy.Spider):

    name               = 'amazon'
    spider_pretty_name = 'Amazon'

    urls = {
        'Blu-ray - Mais vendidos'
            : 'https://www.amazon.com.br/s?i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011',

        'DVD - Mais vendidos'
            : 'https://www.amazon.com.br/s?i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392504011',

        'Busca "SteelBook" - Em destaque'
            : 'https://www.amazon.com.br/s?k=Steelbook&i=dvd&s=relevancerank',

        'Busca "4K" - Em destaque'
            : 'https://www.amazon.com.br/s?k=4K&i=dvd&s=relevancerank',
    }

    start_urls = list(urls.values())

    ignored_categories = [
        'Acessório de telefone sem fio',
        'CD de áudio',
        'Eletrônicos',
        'CD de MP3',
        'CD multimídia',
        'CD-ROM',
        'Cartas',
        'Computadores pessoais',
        'Cozinha',
        'Disco de Vinil',
        'Diversos',
        'Errata ou Retratação de livro',
        'Espiral',
        'Fita cassete',
        'Kindle',
        'Livro cartonado',
        'Luggage',
        'Nintendo Switch',
        'PC',
        'PlayStation 3',
        'PlayStation 4',
        'Produtos de escritório',
        'Vestuário',
        'Videogame',
        'Xbox One',
        'Áudio, Cassete',
        'Nintendo 3DS',
        'PlayStation 5',
        'Relógio',
        'Sony PSP',
        'UMD para PSP',
        'Xbox 360',
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

        result = response.css('.s-result-list > .s-result-item > .sg-col-inner')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            title = movie_selector.css('.a-size-medium > span::text').get().strip()

            cover_url = movie_selector.css('img::attr(src)').get().strip()

            full_title_small_edition, title_type_small_edition, url_small_edition, price_small_edition = \
                self.get_edition_details('.puis-price-instructions-style', movie_selector, response, title)

            if full_title_small_edition is not None:
                if title_type_small_edition not in self.ignored_categories:
                    title_found = {
                        'spider': self.name,
                        'spider_pretty_name': self.spider_pretty_name,
                        'spider_url': response.url,
                        'spider_url_pretty_name': spider_url_pretty_name,
                        'timestamp': timestamp,
                        'full_title': full_title_small_edition,
                        'title': title,
                        'title_type': title_type_small_edition,
                        'url': url_small_edition,
                        'price': price_small_edition,
                        'cover_url': cover_url
                    }
                    log.debug('Title found: {} - {}'.format(full_title_small_edition, price_small_edition))
                    yield title_found
                else:
                    log.debug('Ignoring title due to filter: {}'.format(full_title_small_edition))
            else:
                log.debug('Small edition not found: {}'.format(title))

            full_title_micro_edition, title_type_micro_edition, url_micro_edition, price_micro_edition = \
                self.get_edition_details('.a-spacing-top-mini > .a-row > .a-spacing-mini', movie_selector, response, title, 0)

            if full_title_micro_edition is not None:
                if title_type_micro_edition not in self.ignored_categories:
                    title_found = {
                        'spider': self.name,
                        'spider_pretty_name': self.spider_pretty_name,
                        'spider_url': response.url,
                        'spider_url_pretty_name': spider_url_pretty_name,
                        'timestamp': timestamp,
                        'full_title': full_title_micro_edition,
                        'title': title,
                        'title_type': title_type_micro_edition,
                        'url': url_micro_edition,
                        'price': price_micro_edition,
                        'cover_url': cover_url
                    }
                    log.debug('Title found: {} - {}'.format(full_title_micro_edition, price_micro_edition))
                    yield title_found
                else:
                    log.debug('Ignoring title due to filter: {}'.format(full_title_micro_edition))
            else:
                log.debug('Micro edition not found: {}'.format(title))

            full_title_mini_edition, title_type_mini_edition, url_mini_edition, price_mini_edition = \
                self.get_edition_details('.a-spacing-top-mini > .a-row > .a-spacing-mini', movie_selector, response, title, 1)

            if full_title_mini_edition is not None:
                if title_type_mini_edition not in self.ignored_categories:
                    title_found = {
                        'spider': self.name,
                        'spider_pretty_name': self.spider_pretty_name,
                        'spider_url': response.url,
                        'spider_url_pretty_name': spider_url_pretty_name,
                        'timestamp': timestamp,
                        'full_title': full_title_mini_edition,
                        'title': title,
                        'title_type': title_type_mini_edition,
                        'url': url_mini_edition,
                        'price': price_mini_edition,
                        'cover_url': cover_url
                    }
                    log.debug('Title found: {} - {}'.format(full_title_mini_edition, price_mini_edition))
                    yield title_found
                else:
                    log.debug('Ignoring title due to filter: {}'.format(full_title_mini_edition))
            else:
                log.debug('Mini edition not found: {}'.format(title))

        if self.pagination_enabled:
            next_page = response.css('.s-pagination-next::attr(href)').get()
            if next_page:
                next_page = response.urljoin(next_page.strip())
                log.info('Next page is <{}>'.format(next_page))
                response = self.fetch_page(next_page, spider_url_pretty_name)
                yield from self.parse(response)
            else:
                log.info('Next page not found')
        else:
            log.info('Pagination is disabled')


    def get_edition_details(self, object, selector, response, title, position=0):

        edition = selector.css(object)
        edition = edition[position] if edition is not None and len(edition) > position else None

        header = edition.css('.a-size-base.a-text-bold') if edition is not None else None

        title_type = header.css('::text').get() if header is not None else None
        title_type = title_type.strip() if title_type is not None else None

        if title_type is None:
            return None, None, None, None

        url = header.css('::attr(href)').get()
        url = response.urljoin(url.strip())
        url = url[:url.rfind('/')]

        price = edition.css('.a-offscreen::text').get()
        price = price.strip() if price is not None else 'Indisponível'

        if price != 'Indisponível':
            price = price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
            price = '%.2f' % float(price)

        full_title = title_type + ' - ' + title
        
        return full_title, title_type, url, price


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
