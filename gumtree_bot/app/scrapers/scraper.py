from _ast import ExceptHandler
from app.scrapers.gumtree_scraper_sin import GumtreeScraperSingapore
from app.scrapers.gumtree_scraper_uk import GumtreeScraperUK
from app.scrapers.gumtree_scraper_aus import GumtreeScraperAustralia
from app.scrapers.locanto_scraper_sin import Locanto

from app.models import SearchLog


class Scraper:

    @classmethod
    def validate_data(cls, form_data):
        try:

            if form_data['website'].function == 'gumtree_1':
                return GumtreeScraperSingapore.validate_search(form_data)
            elif form_data['website'].function == 'gumtree_2':
                return GumtreeScraperUK.validate_search(form_data)
            elif form_data['website'].function == 'gumtree_3':
                return GumtreeScraperAustralia.validate_search(form_data)
            elif form_data['website'].function == 'locanto':
                return Locanto.validate_search(form_data)

            raise ValueError('{} function not found for {} '.format(form_data['website'].function,form_data['website']))

        except Exception as ex:
            raise ex

    @classmethod
    def scrap_data(cls, log_id, task_id):
        try:

            search_log = SearchLog.objects.get(pk=int(log_id))

            if search_log.website.function == 'gumtree_1':
                return GumtreeScraperSingapore.extract_ads(search_log, task_id)
            elif search_log.website.function == 'gumtree_2':
                return GumtreeScraperUK.extract_ads(search_log, task_id)
            elif search_log.website.function == 'gumtree_3':
                return GumtreeScraperAustralia.extract_ads(search_log, task_id)
            elif search_log.website.function == 'locanto':
                return Locanto.extract_ads(search_log, task_id)

            raise ValueError('{} function not found for {} '.format(search_log.website.function,
                                                                    search_log.website.name))

        except Exception as ex:
            print(ex)
            raise ex

