import time

import schedule
from scrapy import cmdline


def crawl_aqi():
    cmdline.execute('scrapy runspider /srv/crawler/spiders/iqair.py'.split())


if __name__ == '__main__':
    schedule.every().minute.at(":02").do(crawl_aqi)
    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
        time.sleep(1)
