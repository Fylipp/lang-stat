import lxml.html
import requests

import re

from langstat import urls


def scrape_movie_ids(lang: str):
    """
    Scrapes a bunch of movie ids for the language
    :param lang: The language to find subtitle hashes for
    :return: The found ids
    """
    url = urls.language_page(lang)
    tree = lxml.html.fromstring(requests.get(url).content)

    # The search results table has rows with IDs that consist of 'main' followed by the subtitle hash
    link_ids = tree.xpath('//table[@id="search_results"]/tbody/tr/td/@id')

    return map(lambda e: e[4:], filter(lambda e: len(e) > 4, link_ids))


def scrape_subtitle_id(movie_id):
    """
    Scrapes the subtitle id matching movie id
    :param movie_id:
    :return:
    """
    url = urls.movie_page(movie_id)
    tree = lxml.html.fromstring(requests.get(url).content)

    # Links to the subtitle files are stored in a container
    links = tree.xpath('//*[@id="moviehash"]/a/@href')

    return filter(lambda x: x is not None, map(_extract_id, links))


def _extract_id(subtitle_link):
    """
    Extracts the id of a subtitle link
    :param subtitle_link: The link to the subtitles
    :return: The id contained within the link
    """
    result = re.search(r'/download/+file/+(.*)/?$', subtitle_link, re.IGNORECASE)

    if result is None:
        return None

    return result.group(1)
