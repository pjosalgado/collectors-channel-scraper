# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='collectors-channel-scraper',
    version='$VERSION',
    packages=find_packages(),
    entry_points={
        'scrapy': [
            'settings = movies_shopping_crawler.settings'
        ]
    }
)
