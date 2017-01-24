from _ast import ExceptHandler
from app.scrapers.gumtree_scraper_1 import GumtreeScraperOne


class Scraper:

    @classmethod
    def scrap_data(cls, form_data):
        try:
            if form_data['website'].function == 'gumtree_1':
                return GumtreeScraperOne.validate_search(form_data)

            raise ValueError('{} function not found for {} '.format(form_data['website'].function,form_data['website']))

        except Exception as ex:
            raise ex
