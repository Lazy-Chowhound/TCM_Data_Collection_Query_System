# -*- coding: utf-8 -*-
import scrapy


class RecordspiderSpider(scrapy.Spider):
    name = 'recordSpider'
    allowed_domains = ['https://www.zk120.com/?nav=ys']
    start_urls = ['http://https://www.zk120.com/?nav=ys/']

    def parse(self, response):
        pass
