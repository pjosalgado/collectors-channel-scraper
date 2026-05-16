# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log
from scrapy_playwright.page import PageMethod

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


    def make_request(self, url, spider_url_pretty_name, current_page=1):
        return scrapy.Request(
            url=url,
            meta={
                'spider_url_pretty_name': spider_url_pretty_name,
                'current_page': current_page,
                'playwright': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', 'jet-card'),
                ],
            },
            callback=self.parse,
        )


    async def start(self):
        for name, url in self.urls.items():
            yield self.make_request(url, name)


    def parse(self, response):

        log.info('Visited <{}> - HTTP status: {}'.format(response.url, response.status))

        spider_url_pretty_name = response.meta.get('spider_url_pretty_name', response.url)
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
        current_page = response.meta.get('current_page', 1)

        result = response.css('jet-card .jet-card')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = (movie_selector.css('.product-info h3::text').get() or '').strip()
            title, title_type = self.get_title_details(full_title)

            url = (movie_selector.css('.product-image a::attr(href)').get() or '').strip()
            if url and not url.startswith('http'):
                url = 'https://www.versatilhv.com.br/' + url.lstrip('/')

            price = movie_selector.css('.best-price span::text').get()
            price = price.strip() if price and not movie_selector.css('.product-availability').get() else 'Indisponível'

            if price != 'Indisponível':
                price = price.replace(' ', '').replace('R$', '').replace(',', '.')
                price = '%.2f' % float(price)

            cover_url = (movie_selector.css('.main-image img::attr(src)').get() or '').strip()
            cover_url = 'https:' + cover_url if cover_url.startswith('//') else cover_url

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
                next_page = response.css('a.next-page::attr(href)').get()
                if next_page:
                    next_page = response.urljoin(next_page.strip())
                    log.info('Next page is <{}>'.format(next_page))
                    yield self.make_request(next_page, spider_url_pretty_name, current_page + 1)
                else:
                    log.info('Next page not found')
            else:
                log.info('Max pages reached: {}'.format(self.max_pages))
        else:
            log.info('Pagination is disabled')


    def get_title_details(self, full_title, default_type = 'DVD'):
        if full_title.lower().startswith('blu-ray'):
            title_split = full_title.split(': ', 1)
            return (title_split[1].strip(), title_split[0].strip())
        else:
            return (full_title, default_type)
