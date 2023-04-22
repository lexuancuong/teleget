import logging
import time

import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def crawl_aqi():
    process = CrawlerProcess(get_project_settings())
    process.crawl('iqair')
    logging.info('Crawling AQI...')
    process.start()

if __name__ == '__main__':
    schedule.every().hour.at(":02").do(crawl_aqi)
    while True:
        schedule.run_pending()
        time.sleep(1)
