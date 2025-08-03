# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class VersatilSpider(scrapy.Spider):

    name = 'versatil'
    color_theme_decimal = '15571223'

    start_urls = [
        # Promoção
        'https://www.versatilhv.com.br/categoria/promocao',

        # Raridades
        'https://www.versatilhv.com.br/categoria/raridades',

        # Pré-venda
        'https://www.versatilhv.com.br/categoria/pre-venda',

        # Lançamentos
        'https://www.versatilhv.com.br/categoria/lancamentos',

        # Edições Especiais
        'https://www.versatilhv.com.br/categoria/edicoes-especiais',
    ]


    def parse(self, response): 

        self.log('visited <{}>'.format(response.url))

        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        for movie_selector in response.css('.product-in-card'): 

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

            yield {
                'spider': self.name, 
                'spider_pretty_name': 'Versátil Home Vídeo', 
                'spider_url': response.url, 
                'timestamp': timestamp, 
                'full_title': full_title, 
                'title': title, 
                'title_type': title_type, 
                'url': url, 
                'price': price, 
                'cover_url': cover_url,
                'color_theme_decimal': self.color_theme_decimal
            }


def get_title_details(full_title, default_type = 'DVD'): 
    if full_title.lower().startswith('blu-ray'): 
        title_split = full_title.split(': ', 1)
        return (title_split[1].strip(), title_split[0].strip())
    else: 
        return (full_title, default_type)
