# hellorainbow_scrapper
Scrapping pictures from Pikabu.ru strange user HelloRainbow

# Foreword
There is a mystic user at pikabu.ru community site, that posting pictures of rainbows without any explanations or hints. First rainbows appeared 8 years ago in 2013 and since that time there have been more than 3000 rainbows posted. One rainbow per day. Always. Ever.

# General Description
Here you may find a few scripts that doing several things: parsing @HelloRainbow user posts, extracting the links with images of rainbows, converting them and creating a high resolultion collage with all of the rainbows images found.

# Scripts and usage
0) You may skip the dump links steps 1-3 and go to dump just the images at step 4, using already dumped data.
1) Use the provided settings for the first usage. You may change them later if needed, e.g. for collage better resoluon
2) dump_stories_links.py: parses pikabu.ru for HelloRainbow posts
3) dump_images_links.py: parses the posts with 'Rainbow' title and collects the links to the images (of rainbows, of course)
4) dump_images.py: goes through the collected links and downloads the images
5) process_images.py:  -- convert images to smaller thumbnails, centers them, and creates a collage from the thumbnails.
