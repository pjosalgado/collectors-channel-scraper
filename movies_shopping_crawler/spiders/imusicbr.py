# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class ImusicBrSpider(scrapy.Spider):

    name               = 'imusicbr'
    spider_pretty_name = 'iMusic BR'

    urls = {
        '4K UHD & Blu-ray Steelbooks'
            : 'https://imusic.br.com/exposure/18451/4k-uhd-blu-ray-steelbooks',

        'Filmes da coleção Criterion'
            : 'https://imusic.br.com/exposure/18490/filmes-da-colecao-criterion',

        'Filme 4K UHD'
            : 'https://imusic.br.com/exposure/13562/filme-4k-uhd',

        'Filmes e séries novos e futuros'
            : 'https://imusic.br.com/exposure/29/filmes-e-series-novos-e-futuros',

        'DVD e Blu-ray - Mais Vendido'
            : 'https://imusic.br.com/exposure/11084/dvd-e-blu-ray-mais-vendido',

        'Crunchyroll'
            : 'https://imusic.br.com/exposure/22810/crunchyroll',
    }

    start_urls = list(urls.values())

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

            spider_url_pretty_name = next(
                (name for name, url in self.urls.items() if response.url.startswith(url)),
                response.url  # To do: remove later when it's stable
            )

            if title_type not in self.ignored_categories:
                yield {
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
                    'cover_url': cover_url,
                    'additional_info': '+ ~95% de impostos'
                }

        if self.pagination_enabled:
            next_page = response.css('.navbar-right > .btn-primary')
            next_page = next_page[1].css('::attr(href)').get() if len(next_page) > 0 else None
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')
