import json
import os
import time
from urllib.parse import urlparse
import requests
import settings


def get_filename_from_url(url):
    a = urlparse(url)
    return os.path.basename(a.path)


def dump_all_images(links):
    """ downloading the post first occurred image"""
    curr, n = 0, len(links)
    errors = {}
    for image_link in links:
        print('processing:', curr, 'of', n)
        file_name = get_filename_from_url(image_link)
        path_to_file = settings.images_dir + file_name
        # checking if the file is already exists
        if os.path.exists(path_to_file):
            print(file_name, "exists, skipping")
            curr += 1
            continue
        # if image link is Ok, downloading the file
        if image_link is not None and image_link.endswith(settings.images_extensions):
            img = requests.get(image_link, allow_redirects=True, headers=settings.headers)
            if img.status_code != 200:
                errors[image_link] = "response for the image file is not OK, skipped >> " + image_link
                curr += 1
                continue
            open(path_to_file, 'wb').write(img.content)
        else:
            errors[image_link] = "cannot find image or the found file extension is wrong"
            curr += 1
            continue
        # pausing the requests
        time.sleep(settings.site_request_pause)
        curr += 1
    # print(f'Processed {curr} links')
    return errors


if __name__ == '__main__':
    images_dump_fn = settings.dump_files_dir + settings.images_links_dump_fname
    images_links_dict = json.load(open(images_dump_fn, "r"))
    # total links
    links_n = len(images_links_dict.values())
    # unique links
    links_unique = set(images_links_dict.values())
    links_unique_n = len(links_unique)
    # dumping images
    errors = dump_all_images(links_unique)
    print(f'Total loaded links: {links_n}. Unique: {links_unique_n}')
    print("errors: ", errors)
