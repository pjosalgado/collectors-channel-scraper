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


    def parse(self, response): 

        self.log('visited <{}>'.format(response.url))

        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        for movie_selector in response.css('.filmes-e-series'): 

            full_title = movie_selector.css('h3 > a::text').get().strip()
            title, title_type = get_title_details(full_title)

            url = movie_selector.css('h3 > a::attr(href)').get().strip()

            price = movie_selector.css('.newPrice::text').get()
            price = movie_selector.css('.bestPrice > em::text').get() if price is None else price
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível': 
                price = price.replace(' ', '').replace('R$', '').replace(',', '.')
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('img::attr(src)').get().strip()

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


def get_title_details(full_title, default_type = 'Desconhecido'): 
    title_split = full_title.split(' - ', 1)
    return (title_split[1].strip(), title_split[0].strip()) if len(title_split) == 2 else (full_title, default_type)
