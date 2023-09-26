# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import pytz

class AmazonSpider(scrapy.Spider): 

    name = 'amazon'

    start_urls = [
        # Blu-ray - Popularidade
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=popularity-rank&dc&rnid=19392499011&ref=sr_st_popularity-rank&ds=v1%3AacIgbzmOjSmDNVsO5jUcv3O6m%2BltVqwiWDouNHSFPAI',

        # Blu-ray - Preço: baixo a alto
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=price-asc-rank&dc&rnid=19392499011&ref=sr_st_price-asc-rank&ds=v1%3A0nHoSC0DFthpCVCWowU6jd0My6y%2BOLss%2Fim2hxigksM',

        # Blu-ray - Avaliação dos clientes (média)
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=review-rank&dc&rnid=19392499011&ref=sr_st_review-rank&ds=v1%3AVo%2BB8f211fCNbbqcXbHRCaQ1PngevKwUmtSs%2BO3Kmmc',

        # Blu-ray - Data de lançamento
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392502011&s=date-desc-rank&dc&rnid=19392499011&ref=sr_st_date-desc-rank&ds=v1%3AgoepJFYF%2BY9brRUB9JMVMHEYacuIvZ5HbSVN1w%2BChjI',

        # DVD - Popularidade
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392504011&s=popularity-rank&dc&rnid=19392499011&ref=sr_st_popularity-rank&ds=v1%3AiGwzt4iz80dTecPkbgNkJPd4HD7tn1nw8nb07%2Bu7Cj8',

        # DVD - Preço: baixo a alto
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392504011&s=price-asc-rank&dc&rnid=19392499011&ref=sr_st_price-asc-rank&ds=v1%3AtVcgC7vxmjK03ClKtEGBKvydM%2F8G1bB%2BAWpsXXS1roo',

        # DVD - Avaliação dos clientes (média)
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392504011&s=review-rank&dc&rnid=19392499011&ref=sr_st_review-rank&ds=v1%3AONLj%2Bmx%2ByW38VYFsMwFpvruY0n1EKoWTuUfkxonslAI',

        # DVD - Data de lançamento
        'https://www.amazon.com.br/s?i=dvd&bbn=7791856011&rh=n%3A7791856011%2Cp_n_binding_browse-bin%3A19392504011&s=date-desc-rank&dc&rnid=19392499011&ref=sr_st_date-desc-rank&ds=v1%3AaVBJzfs9wGav2eXqoPRXgzEjh2zPHGLnZGIk9kLbXtI',

        # Busca "SteelBook" - Destaques
        'https://www.amazon.com.br/s?k=Steelbook&i=dvd&ref=nb_sb_ss_ts-doa-p_2_4',

        # Busca "SteelBook" - Preço: baixo a alto
        'https://www.amazon.com.br/s?k=Steelbook&i=dvd&s=price-asc-rank&ref=sr_st_price-asc-rank&ds=v1%3Am9Gmh7Y6XB7Olkf9%2BcdLhdCT3He95JMtRr7UI0rnmNs',

        # Busca "SteelBook" - Avaliação dos clientes (média)
        'https://www.amazon.com.br/s?k=Steelbook&i=dvd&s=review-rank&ref=sr_st_review-rank&ds=v1%3AZCBb3OekUtQ6cRr2CzeHUlYZK2dfieBfO9vIJtELLew',

        # Busca "SteelBook" - Data de lançamento
        'https://www.amazon.com.br/s?k=Steelbook&i=dvd&s=date-desc-rank&ref=sr_st_date-desc-rank&ds=v1%3AQZoIeIQms2le9YUVuUJuq6n9AgqnVQC5qPHJ%2F80wFbk',

        # Busca "4K" - Destaques
        'https://www.amazon.com.br/s?k=4K&i=dvd&s=relevancerank&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=sr_st_relevancerank&ds=v1%3ATYqaoTfv1pNBrMcY8%2BmfDipx0297McbkQLaHkOTqO5I',

        # Busca "4K" - Preço: baixo a alto
        'https://www.amazon.com.br/s?k=4K&i=dvd&s=price-asc-rank&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=sr_st_price-asc-rank&ds=v1%3AyXqSDvKRgAP08INdzUDwGtWuUXGh6bdhxNSkKEqOMKs',

        # Busca "4K" - Avaliação dos clientes (média)
        'https://www.amazon.com.br/s?k=4K&i=dvd&s=review-rank&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=sr_st_review-rank&ds=v1%3AXMWJ8JjsGkGzdGuovrAtl0iIvNBWzD8iGqKojdwUQgg',

        # Busca "4K" - Data de lançamento
        'https://www.amazon.com.br/s?k=4K&i=dvd&s=date-desc-rank&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=sr_st_date-desc-rank&ds=v1%3A3rfglGb3u%2FGs1nKm6z4znU8lHazi%2Bj9oZOp5bMAHfdc',
    ]

    ignored_categories = [
        'Acessório de telefone sem fio', 
        'CD de áudio', 
        'Eletrônicos',
        'CD de MP3',
        'CD multimídia',
        'CD-ROM',
        'Cartas',
        'Computadores pessoais',
        'Cozinha',
        'Disco de Vinil',
        'Diversos',
        'Errata ou Retratação de livro',
        'Espiral',
        'Fita cassete',
        'Kindle',
        'Livro cartonado',
        'Luggage',
        'Nintendo Switch',
        'PC',
        'PlayStation 3',
        'PlayStation 4',
        'Produtos de escritório',
        'Vestuário',
        'Videogame',
        'Xbox One',
        'Áudio, Cassete'
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

        result = response.css('.s-result-list > .s-result-item > .sg-col-inner')
        self.log('{} movies found'.format(len(result)))

        for movie_selector in result: 
            
            title = movie_selector.css('.a-size-medium::text').get().strip()

            cover_url = movie_selector.css('img::attr(src)').get().strip()

            full_title_small_edition, title_type_small_edition, url_small_edition, price_small_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-small', movie_selector, response, title)

            if full_title_small_edition is not None: 
                if title_type_small_edition not in self.ignored_categories: 
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
                else: 
                    self.log('ignoring title due to filter {} - {}'.format(title_type_small_edition, full_title_small_edition))

            full_title_micro_edition, title_type_micro_edition, url_micro_edition, price_micro_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-micro', movie_selector, response, title)

            if full_title_micro_edition is not None: 
                if title_type_micro_edition not in self.ignored_categories: 
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
                else: 
                    self.log('ignoring title due to filter {} - {}'.format(title_type_micro_edition, full_title_micro_edition))

            full_title_mini_edition, title_type_mini_edition, url_mini_edition, price_mini_edition = \
                get_edition_details('.a-section.a-spacing-none.a-spacing-top-mini', movie_selector, response, title)

            if full_title_mini_edition is not None: 
                if title_type_mini_edition not in self.ignored_categories: 
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
                else: 
                    self.log('ignoring title due to filter {} - {}'.format(title_type_mini_edition, full_title_mini_edition))

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
