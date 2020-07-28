# THIS FILE HOLDS THE FUNCTIONS THAT INTERACT WITH THE OPEN FOOD FACT API

import urllib.parse
from math import ceil
import requests


def create_search_url(page, category):
    """
        This function creates the search url for a specified category and page number
            page : int
            category : str
            url : str
    """

    parameters = {
        'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': category,
        'page_size': 100,
        'page': page,
        'json': '1'
    }
    url = 'https://fr.openfoodfacts.org/cgi/search.pl?' + urllib.parse.urlencode(parameters)

    return url


def get_pages_count(category):
    """
        This function retrieves the amount of result pages for a specified category
            category : str
            page_amount : int
    """

    url = create_search_url('1', category)

    request = requests.get(url)
    data = request.json()
    page_amount = ceil(int(data['count']) / 100)

    return page_amount


def get_products(page, category):
    """
        This function retrieves the final products of a specified page number and category by using the other functions
            page : int
            category : str
            return : list
    """
    return requests.get(create_search_url(page, category)).json()['products']
