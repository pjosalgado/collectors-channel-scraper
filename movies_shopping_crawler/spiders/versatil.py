# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class VersatilSpider(scrapy.Spider): 

    name = 'versatil'

    start_urls = [
        # Lançamentos
        'https://www.versatilhv.com.br/categoria/lancamentos',

        # Pré-venda de filmes
        'https://www.versatilhv.com.br/categoria/pre-venda',

        # Edições Especiais
        'https://www.versatilhv.com.br/categoria/edicoes-especiais',

        # Promoção
        'https://www.versatilhv.com.br/categoria/promocao',

        # Blu-Ray
        'https://www.versatilhv.com.br/categoria/blu-ray',

        # Clássicos Sci-FI
        'https://www.versatilhv.com.br/categoria/colecoes/classicos-sci-fi',

        # Filmes Coleção Folha
        'https://www.versatilhv.com.br/categoria/colecoes/colecao-folha',

        # Lovecraft No Cinema
        'https://www.versatilhv.com.br/categoria/colecoes/lovecraft-no-cinema',

        # Cinema Asiático
        'https://www.versatilhv.com.br/categoria/colecoes/cinema-asiatico',

        # Cinema Samurai
        'https://www.versatilhv.com.br/categoria/colecoes/cinema-samurai',

        # Cinema Brasileiro
        'https://www.versatilhv.com.br/categoria/colecoes/cinema-brasileiro',

        # Cinema Kung Fu
        'https://www.versatilhv.com.br/categoria/colecoes/cinema-kung-fu',

        # Cinema Yakuza
        'https://www.versatilhv.com.br/categoria/colecoes/cinema-yakuza',

        # Akira Kurosawa
        'https://www.versatilhv.com.br/categoria/diretores/akira-kurosawa',

        # Lars Von Trier
        'https://www.versatilhv.com.br/categoria/diretores/lars-von-trier',

        # Alfred Hitchcock
        'https://www.versatilhv.com.br/categoria/diretores/alfred-hitchcock',

        # Glauber Rocha
        'https://www.versatilhv.com.br/categoria/diretores/glauber-rocha',
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
                'cover_url': cover_url
            }


def get_title_details(full_title, default_type = 'DVD'): 
    if full_title.lower().startswith('blu-ray'): 
        title_split = full_title.split(': ', 1)
        return (title_split[1].strip(), title_split[0].strip())
    else: 
        return (full_title, default_type)
