# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class VideoPerolaSpider(scrapy.Spider): 

    name = 'videoperola'

    start_urls = [
        # Exclusivos
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/exclusivos/',

        # Lançamentos
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/lancamentos/',

        # Pré-Venda
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/pre-venda/',

        # Blu-ray 3D
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/blu-ray-3d/',

        # Steelbook
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/steelbook/',

        # Coleções
        'https://videoperola.com.br/todas-as-categorias/filmes-e-series/colecoes/',
        
        # Busca "4K"
        'https://videoperola.com.br/search/?q=4K',
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

        for movie_selector in response.css('.js-item-product'): 

            full_title = movie_selector.css('.item-name::text').get().strip()
            title, title_type = get_title_details(full_title)

            url = movie_selector.css('.item-link::attr(href)').get().strip()

            price = movie_selector.css('.item-price-secondary::text').get()
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível': 
                price = price.replace(' ', '').replace('R$', '').replace(',', '.').replace('por', '').replace('\n', '').strip()
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('.js-item-image::attr(data-srcset)').get().strip()
            cover_url = cover_url.split(' ')[0]
            cover_url = 'https:' + cover_url

            yield {
                'spider': self.name, 
                'spider_pretty_name': 'Vídeo Pérola', 
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
            next_page = response.css('.pagination-arrow-link::attr(href)').get()
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')


def get_title_details(full_title, default_type = 'Desconhecido'): 
    title_split = full_title.split(' - ', 1)
    return (title_split[1].strip(), title_split[0].strip()) if len(title_split) == 2 else (full_title, default_type)
