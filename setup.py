from setuptools import setup

readme = open('./README.md', 'r')

setup(
    name = 'bowlsRecipeScraper',
    version = '0.1.0',
    packages = ['bowlsRecipeScraper'],
    description = 'A Python package to scrap recipes from bowl of delicious website',
    long_description = readme.read(),
    long_description_content_type = 'text/markdown',
    author = 'Valeria Gonzalez',
    author_email = 'valeriasegura33@gmail.com',
    url = 'https://github.com/valeria-gonzalez/BowlsRecipeScraper',
    keywords=['scraper', 'recipe', 'web scraper', 'bowls of delicious'],
    classifiers = [],
    license = 'MIT',
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'requests',
        'recipe-scrapers',
        'selenium',
        'webdriver-manager'
    ]
)