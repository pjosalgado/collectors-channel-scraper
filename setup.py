# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name = 'project',
    version = '2.6.1',
    packages = find_packages(),
    entry_points = {
        'scrapy': [
            'settings = movies_shopping_crawler.settings'
        ]
    }
)
