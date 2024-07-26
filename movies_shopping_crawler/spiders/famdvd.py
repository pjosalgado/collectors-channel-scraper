# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class FamDvdSpider(scrapy.Spider): 

    name = 'famdvd'

    start_urls = [
        # Exclusivos
        'https://www.famdvd.com.br/exclusivos-1.html', 

        # Lançamentos
        'https://www.famdvd.com.br/lancamento.html', 

        # Pré-venda
        'https://www.famdvd.com.br/pre-venda.html', 

        # Busca "4K"
        'https://www.famdvd.com.br/catalogsearch/result/?q=4K',
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

        for movie_selector in response.css('li.item'): 
            
            full_title = movie_selector.css('h3 > a::text').get().strip()
            title, title_type = get_title_details(full_title)

            url = movie_selector.css('h3 > a::attr(href)').get().strip()
            
            price = movie_selector.css('.special-price > .price::text').get()
            price = movie_selector.css('.price::text').get() if price is None else price
            price = price.strip() if price is not None else 'Indisponível'

            if price != 'Indisponível': 
                price = price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
                price = '%.2f' % float(price)

            cover_url = movie_selector.css('img::attr(src)').get().strip()
            
            yield {
                'spider': self.name, 
                'spider_pretty_name': 'Fam DVD', 
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
            next_page = response.css('.i-next::attr(href)').get()
            if next_page: 
                next_page = next_page.strip()
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')


def get_title_details(full_title, default_type = 'DVD'): 
    if full_title.lower().startswith('blu-ray'): 
        title_split = full_title.split(' - ', 1)
        return (title_split[1].strip(), title_split[0].strip())
    else: 
        return (full_title, default_type)
