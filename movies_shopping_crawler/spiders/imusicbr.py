# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class ImusicBrSpider(scrapy.Spider): 

    name = 'imusicbr'

    start_urls = [
        # Filmes da Criterion Collection
        'https://imusic.br.com/exposure/18490/filmes-da-colecao-criterion',

        # 4K UHD Movies
        'https://imusic.br.com/exposure/13562/4k-uhd-movies',

        # Filmes e séries novos e futuros
        'https://imusic.br.com/exposure/29/filmes-e-series-novos-e-futuros',

        # DVDs e Blu-rays em estoque
        'https://imusic.br.com/exposure/1717/dvd-s-and-blu-rays-in-stock',

        # DVD e Blu-ray - Mais Vendido
        'https://imusic.br.com/exposure/11084/dvd-e-blu-ray-mais-vendido',
    ]

    ignored_categories = [
        'Paperback Book',
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

        for movie_selector in response.css('.item-teaser'): 

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
                yield {
                    'spider': self.name, 
                    'spider_pretty_name': 'iMusic BR', 
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
            next_page = response.css('.navbar-right > .btn-primary')
            next_page = next_page[1].css('::attr(href)').get() if len(next_page > 1) else None
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')
