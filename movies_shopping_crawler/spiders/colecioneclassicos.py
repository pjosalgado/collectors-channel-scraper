# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class ColecioneClassicosSpider(scrapy.Spider):

    name = 'colecioneclassicos'
    color_theme_decimal = '13608282'

    start_urls = [
        # Box e Coleções
        'https://www.colecioneclassicos.com.br/box-e-colecoes',

        # Destaques Imperdíveis
        'https://www.colecioneclassicos.com.br/de-volta-a-loja',

        # Obras-Primas do Cinema
        'https://www.colecioneclassicos.com.br/OP',

        # Pré-Venda
        'https://www.colecioneclassicos.com.br/pre-venda',

        # Lançamentos
        'https://www.colecioneclassicos.com.br/lancamentos',

        # Busca "4K"
        'https://www.colecioneclassicos.com.br/buscar?q=4K',
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
                'spider_pretty_name': 'Colecione Clássicos', 
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

        if self.pagination_enabled: 
            next_page = response.css('a[rel=next]::attr(href)').get()
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')


def get_title_type(full_title, default_type = 'DVD'): 
    full_title = full_title.lower().replace('-', '').replace(' ', '')
    if 'bluray' in full_title or 'bd' in full_title: 
        return 'Blu-ray'
    else: 
        return default_type
