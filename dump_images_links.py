import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import settings


def get_image_link_from_soup(soup):
    """ returns a first found link to image in the soup """
    img_link = soup.find('img', attrs={'class': ['story-image__image', 'image-loaded']})['data-large-image']
    return img_link


def dump_images_links(links):
    """ parses stories links and dumps a dictionary of 'story_link: image_link' to a file """

    # open a links dump file or create if doesn't exist
    fn = settings.dump_files_dir + settings.images_links_dump_fname
    try:
        with open(fn, 'r') as fp:
            stories_links_and_links_to_images = json.load(fp)
            print("Links to images loaded, size:", len(stories_links_and_links_to_images.items()))
    except IOError:
        print("Links to images file is not found, creating a new one")
        stories_links_and_links_to_images = {}

    errors = {}
    n, counter = len(links), 0

    for link in links:
        print('** Processing:', counter, 'of', n, link)
        # if a story link in the dump file, skipping
        if link in stories_links_and_links_to_images.keys():
            print("  >> Link exist in the dump file, skipping")
            counter += 1
            continue
        # getting a post soup
        response = requests.get(link, headers=settings.headers)
        if response.status_code != 200:
            print("  !! response is not OK for url:", link)
            counter += 1
            errors[link] = "response for the story url is not OK, skipped"
            continue
        soup = BeautifulSoup(response.text, features="html.parser")
        # getting a link for the image
        stories_links_and_links_to_images[link] = get_image_link_from_soup(soup)
        # dumping the links
        fn = settings.dump_files_dir + settings.images_links_dump_fname
        with open(fn, 'w') as fp:
            json.dump(stories_links_and_links_to_images, fp)
        counter += 1
    print(f'Processed {counter} files')
    return errors


if __name__ == '__main__':
    # open stories links dump file
    links_and_titles_fn = settings.dump_files_dir + settings.stories_links_dump_fname
    links_and_titles_dict = json.load(open(links_and_titles_fn, "r"))
    # print some data
    df = pd.DataFrame(links_and_titles_dict.items(), columns=['link', 'story_name'])
    print("Total posts number: ", len(df))
    df = df[df.story_name == settings.story_title_to_scrap]
    print(f"Posts with {settings.story_title_to_scrap} title number: {len(df)}")

    # dumping links of images for the posts with "Rainbow" title
    errors = dump_images_links(df.link)
    print("errors: ", errors)
