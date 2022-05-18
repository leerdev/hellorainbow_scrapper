import requests
import time
import json
from bs4 import BeautifulSoup
import settings


def get_next_page_link(soup):
    """ returns a link to the next page from the current page soup
        or None if not found (the page is the last one) """
    ret = soup.find('a', attrs={'class': 'pagination__page pagination__page_next'})
    if ret is None:
        return None
    return ret['href']


def get_current_links(soup):
    """ returns a dict of posts links as keys and name of the posts as values"""
    titles = soup.find_all('h2', attrs={'class': 'story__title'})  # finding all titles of the stories on page
    if (titles is None) or (len(titles) == 0):
        return None
    links_and_titles = {
        el.find('a')['href']: el.find('a').text for el in titles
    }
    return links_and_titles


def scrap_for_links(url):
    """ main function to loop over the found pages and
    dump all links to the posts into a file as json"""
    links_and_titles = {}
    while True:
        print(f'Processing link', url, end=" >>> ")
        response = requests.get(url, headers=settings.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            current_page_links = get_current_links(soup)
            links_and_titles.update(get_current_links(soup))
            print(len(current_page_links))
            url = get_next_page_link(soup)
            if url is None:
                return links_and_titles
            time.sleep(settings.site_request_pause)


# entry point
if __name__ == '__main__':
    # getting links to the stories
    links_and_titles_dict = scrap_for_links(url=settings.starting_url)
    # and dumping them
    print(">>> Dumping links, size of:", len(links_and_titles_dict.items()))
    dump_file_name = settings.dump_files_dir + settings.stories_links_dump_fname
    json.dump(links_and_titles_dict, open(dump_file_name, "w"))
