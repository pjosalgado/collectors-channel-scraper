# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class AmazonSpider(scrapy.Spider): 

    name = 'amazon'

    start_urls = [
        # Popularidade
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011&s=popularity-rank&dc&qid=1608958148&ref=sr_st_popularity-rank', 
        # Data de lançamento
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011&s=date-desc-rank&dc&qid=1608958152&ref=sr_st_date-desc-rank', 
        # Ofertas do Dia - Popularidade
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_specials_match%3A21225669011&s=popularity-rank&dc&qid=1608958301&rnid=21225668011&ref=sr_st_popularity-rank', 
        # Ofertas do Dia - Data de lançamento
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_specials_match%3A21225669011&s=date-desc-rank&dc&qid=1608958230&rnid=21225668011&ref=sr_st_date-desc-rank', 
        # 4K - Destaques
        'https://www.amazon.com.br/s?k=4k&i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1608960350&rnid=19392499011&ref=sr_nr_p_n_binding_browse-bin_1', 
        # 4K - Preço: baixo a alto
        'https://www.amazon.com.br/s?k=4k&i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=price-asc-rank&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1608960708&rnid=19392499011&ref=sr_st_price-asc-rank', 
        # UHD - Destaques
        'https://www.amazon.com.br/s?k=uhd&i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1608960365&rnid=19392499011&ref=sr_nr_p_n_binding_browse-bin_1', 
        # UHD - Preço: baixo a alto
        'https://www.amazon.com.br/s?k=uhd&i=dvd&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=price-asc-rank&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1608960743&rnid=19392499011&ref=sr_st_price-asc-rank'
    ]

    ignored_categories = ['Acessório de telefone sem fio', 'CD de áudio', 'Eletrônicos']


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

        result = response.css('.s-result-list > .s-result-item > .sg-col-inner')
        self.log('{} movies found'.format(len(result)))

        for movie_selector in result: 
            
            title = movie_selector.css('.a-size-medium::text').get().strip()

            cover_url = movie_selector.css('img::attr(src)').get().strip()

            full_title_small_edition, title_type_small_edition, url_small_edition, price_small_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-small', movie_selector, response, title)

            if full_title_small_edition is not None and title_type_small_edition not in self.ignored_categories: 
                yield {
                    'spider': self.name, 
                    'spider_pretty_name': 'Amazon', 
                    'spider_url': response.url, 
                    'timestamp': timestamp, 
                    'full_title': full_title_small_edition, 
                    'title': title, 
                    'title_type': title_type_small_edition, 
                    'url': url_small_edition, 
                    'price': price_small_edition, 
                    'cover_url': cover_url
                }

            full_title_micro_edition, title_type_micro_edition, url_micro_edition, price_micro_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-micro', movie_selector, response, title)

            if full_title_micro_edition is not None and title_type_micro_edition not in self.ignored_categories: 
                yield {
                    'spider': self.name, 
                    'spider_pretty_name': 'Amazon', 
                    'spider_url': response.url, 
                    'timestamp': timestamp, 
                    'full_title': full_title_micro_edition, 
                    'title': title, 
                    'title_type': title_type_micro_edition, 
                    'url': url_micro_edition, 
                    'price': price_micro_edition, 
                    'cover_url': cover_url
                }

            full_title_mini_edition, title_type_mini_edition, url_mini_edition, price_mini_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-mini', movie_selector, response, title)

            if full_title_mini_edition is not None and title_type_mini_edition not in self.ignored_categories: 
                yield {
                    'spider': self.name, 
                    'spider_pretty_name': 'Amazon', 
                    'spider_url': response.url, 
                    'timestamp': timestamp, 
                    'full_title': full_title_mini_edition, 
                    'title': title, 
                    'title_type': title_type_mini_edition, 
                    'url': url_mini_edition, 
                    'price': price_mini_edition, 
                    'cover_url': cover_url
                }

        if self.pagination_enabled: 
            next_page = response.css('.a-last > a::attr(href)').get()
            if next_page: 
                next_page = response.urljoin(next_page.strip())
                self.log('next page is <{}>'.format(next_page))
                yield scrapy.Request(next_page)
            else: 
                self.log('next page not found')


def get_edition_details(object, selector, response, title): 

    edition = selector.css(object)
    edition = edition[0] if edition is not None and len(edition) > 0 else None

    header = edition.css('.a-size-base.a-text-bold') if edition is not None else None

    title_type = header.css('::text').get() if header is not None else None
    title_type = title_type.strip() if title_type is not None else None

    if title_type is None: 
        return None, None, None, None

    url = header.css('::attr(href)').get()
    url = response.urljoin(url.strip())
    url = url[:url.rfind('/')]

    price = edition.css('.a-offscreen::text').get()
    price = price.strip() if price is not None else 'Indisponível'

    if price != 'Indisponível': 
        price = price.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
        price = '%.2f' % float(price)

    full_title = title_type + ' - ' + title
    
    return full_title, title_type, url, price
