# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz
import logging as log

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


    def parse(self, response):

        log.info('Visited <{}>'.format(response.url))

        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        result = response.css('.product-in-card')
        log.info('{} titles found'.format(len(result)))

        for movie_selector in result:

            full_title = movie_selector.css('h3 > span::text').get().strip()
            title, title_type = get_title_details(full_title)

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

            spider_url_pretty_name = next(
                (name for name, url in self.urls.items() if response.url.startswith(url)),
                response.url  # To do: remove later when it's stable
            )

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


def get_title_details(full_title, default_type = 'DVD'):
    if full_title.lower().startswith('blu-ray'):
        title_split = full_title.split(': ', 1)
        return (title_split[1].strip(), title_split[0].strip())
    else:
        return (full_title, default_type)
