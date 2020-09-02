from SeleniumDriver import SeleniumDriver
from Scraper import Scraper
import os

if __name__ == '__main__':
    # Create the browser
    browser = SeleniumDriver.get_instance()

    # Read urls to scrape from the input files
    input_files_path = './input-files'
    urls = set()
    for input_file in os.listdir(input_files_path):
        with open(os.path.join(input_files_path, input_file), 'r') as f:
            lines = f.readlines()
            urls.update(lines)

    # Start scraping
    for url in urls:
        nation, league = url.split('/')[4:6]
        pickle_name = '{}_{}.pkl'.format(nation, league)
        if os.path.isfile('./output-pickles/{}'.format(pickle_name)):
            print('File for {}-{} already exists'.format(nation, league))
        else:
            print('Scraping from url {}'.format(url))
            scraper = Scraper(browser, url)
            del scraper

