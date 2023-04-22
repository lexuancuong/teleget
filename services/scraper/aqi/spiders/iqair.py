import scrapy
from scrapy.http import JsonRequest, TextResponse
from twisted.python.failure import Failure


class IQAIRSpider(scrapy.Spider):
    name = "iqair"
    start_urls_dict = {
        # url : (lat, long)
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/us-consulate-in-ho-chi-minh-city': (
            10.782308,
            106.701878,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/thao-dien': (
            10.810894,
            106.731490,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/saigon-star-international-school': (
            10.765792,
            106.760986,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/saigon-south-international-school': (
            10.722078,
            106.708870,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/aqsea_vn_032': (
            10.732977,
            106.633965,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/lycee-francais-international-marguerite-duras': (
            10.870270,
            106.825064,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/the-abc-international-school-trung-son-campus': (
            10.733827,
            106.693225,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/225-nguyen-van-huong-d2': (
            10.812595,
            106.732179,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/the-abc-international-nha-be-campus': (
            10.721850,
            106.704664,
        ),
        'https://www.iqair.com/vi/vietnam/ho-chi-minh-city/mam-non-hai-au-bay': (
            10.795300,
            106.675032,
        ),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = list(self.start_urls_dict.keys())

    def parse(self, response: TextResponse):
        aqi = response.css('p.aqi-value__value::text').extract_first()
        pm25 = response.css(
            'span.mat-tooltip-trigger.pollutant-concentration-value::text'
        ).extract_first()
        temperature = response.css(
            'div.weather__detail > table > tbody > tr:nth-child(2) > td:nth-child(2)::text'
        ).extract_first()
        if temperature:
            temperature = temperature.replace('°C', '')
        humidity = response.css(
            'div.weather__detail > table > tbody > tr:nth-child(3) > td:nth-child(2)::text'
        ).extract_first()
        if humidity:
            humidity = humidity.replace('%', '')
        warning = response.css(
            'div > app-timestamp-late > p > span.tag::text'
        ).extract_first()
        request_body = {
            **dict(
                aqi=aqi,
                pm25=pm25,
                temperature=temperature,
                humidity=humidity,
                active=not bool(warning),
            ),
            'location': {
                'lat': self.start_urls_dict[response.url][0],
                'long': self.start_urls_dict[response.url][1],
            },
        }
        yield JsonRequest(
            'http://api:8000/api/aqi/',
            data=request_body,
            callback=self.post_air_info_successfully,
        )

    def post_air_info_successfully(self, response: TextResponse):
        print(f"Posted air info successfully {response.json()}")

    def post_air_info_failure(self, err: Failure):
        print(f"Failed to post air info because {err.getTraceback()}")
