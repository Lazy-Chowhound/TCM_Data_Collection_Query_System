# -*- coding: utf-8 -*-
import scrapy


class ZybdSpider(scrapy.Spider):
    name = 'zybd'
    allowed_domains = ['http://zhongyibaodian.com/yian/']
    start_urls = ['http://http://zhongyibaodian.com/yian//']

    def parse(self, response):
        pass
