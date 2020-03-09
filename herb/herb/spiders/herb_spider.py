# -*- coding: utf-8 -*-
import scrapy


class HerbSpiderSpider(scrapy.Spider):
    name = 'herb_spider'
    allowed_domains = ['https://www.zyctd.com/data/ycgx.html']
    start_urls = ['http://https://www.zyctd.com/data/ycgx.html/']

    def parse(self, response):
        pass
