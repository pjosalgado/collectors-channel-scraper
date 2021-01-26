# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class TheOriginalsSpider(scrapy.Spider):

    name = 'theoriginals'

    start_urls = [
        'https://www.theoriginals.com.br/filmes-pre-venda', 
        'https://www.theoriginals.com.br/filmes-lancamentos', 
        'https://www.theoriginals.com.br/filmes-promocoes', 
        'https://www.theoriginals.com.br/filmes-promocoes-de-dvd', 
        'https://www.theoriginals.com.br/filmes-promocoes-em-blu-ray', 
        'https://www.theoriginals.com.br/filmes-promocoes-em-blu-ray-3d', 
        'https://www.theoriginals.com.br/filmes-promocoes-series-e-colecoes'
    ]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs): 

        try: 
            pagination_enabled = kwargs['PAGINATION_ENABLED'] == "True"
        except: 
            pagination_enabled = False
        
        spider = cls(
            *args, 
            pagination_enabled=pagination_enabled, 
            **kwargs
        )
        
        spider._set_crawler(crawler)
        
        return spider


    def parse(self, response):

        self.log('visited <{}>'.format(response.url))

        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        for movie_selector in response.css('.listagem-item'): 

            full_title = movie_selector.css('.nome-produto::text').get().strip()
            title = full_title
            title_type = get_title_type(full_title)

            url = movie_selector.css('.produto-sobrepor::attr(href)').get().strip()
            
            price = movie_selector.css('.preco-promocional::text').get()
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível': 
                price = price.replace(' ', '').replace('R$', '').replace(',', '.')
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('img::attr(src)').get().strip()

            yield {
                'spider': self.name, 
                'spider_pretty_name': 'The Originals', 
                'spider_url': response.url, 
                'timestamp': timestamp, 
                'full_title': full_title, 
                'title': title, 
                'title_type': title_type, 
                'url': url, 
                'price': price, 
                'cover_url': cover_url
            }

        if self.pagination_enabled: 
            next_page = response.css('a[rel=next]::attr(href)').get()
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')


def get_title_type(full_title, default_type = 'Desconhecido'): 
    full_title = full_title.lower().replace('-', '').replace(' ', '')
    if 'bluray' in full_title or 'steelbook' in full_title: 
        return 'Blu-ray'
    elif 'dvd' in full_title: 
        return 'DVD'
    else: 
        return default_type
