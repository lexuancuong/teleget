# -*- coding: utf-8 -*-
import random

import scrapy
from scrapy.http import JsonRequest


class IQAIRSpider(scrapy.Spider):
    name = "iqair"
    start_urls_dict = {
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/us-consulate-in-ho-chi-minh-city': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/thao-dien': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/saigon-star-international-school': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/saigon-south-international-school': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/aqsea_vn_032': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/lycee-francais-international-marguerite-duras': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/the-abc-international-school-trung-son-campus': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/225-nguyen-van-huong-d2': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/the-abc-international-nha-be-campus': (
            10,
            random.randint(0, 100),
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/mam-non-hai-au-bay': (
            10,
            random.randint(0, 100),
        ),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = list(self.start_urls_dict.keys())

    def parse(self, response):
        request_body = {
            'aqi': response.css(
                '#content-wrapper > app-routes-resolver > div > app-station > div.container.content__wrapper.ng-star-inserted > div.right-side > app-aqi-overview > div > div.aqi-orange.aqi-overview__summary > div > div > p.aqi-value__value::text'
            ).extract_first(),
            'pm25': response.css(
                '#content-wrapper > app-routes-resolver > div > app-station > div.container.content__wrapper.ng-star-inserted > div.right-side > app-aqi-overview > div > div.aqi-overview-detail > table > tbody > tr > td:nth-child(3) > span.mat-tooltip-trigger.pollutant-concentration-value::text'
            ).extract_first(),
            'temperature': response.css(
                '#content-wrapper > app-routes-resolver > div > app-station > div.container.content__wrapper > div.left-side > app-weather > div > div.weather__detail > table > tbody > tr:nth-child(2) > td:nth-child(2)::text'
            ).extract_first(),
            'humidity': response.css(
                '#content-wrapper > app-routes-resolver > div > app-station > div.container.content__wrapper > div.left-side > app-weather > div > div.weather__detail > table > tbody > tr:nth-child(3) > td:nth-child(2)::text'
            ).extract_first(),
            'lat': self.start_urls_dict.get(response.url)[0],
            'long': self.start_urls_dict.get(response.url)[1],
        }
        yield JsonRequest(
            'http://api:8000/api/aqi/',
            data=request_body,
            errback=self.error_call_back,
        )

    def error_call_back(self, err):
        breakpoint()
