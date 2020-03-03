# -*- coding: utf-8 -*-
import scrapy
import mysql.connector
import requests
from lxml import etree


class PrescriptionspiderSpider(scrapy.Spider):
    name = 'prescriptionSpider'
    # allowed_domains = ['http://www.zysj.com.cn']
    start_urls = ['http://www.zysj.com.cn/zhongyaofang/index_9.html']
    # url = "http://www.zysj.com.cn/zhongyaofang/index_{0}.html"

    # page = 1
    # maxpage = 2

    connection = None
    cursor = None

    def format_value(self, list):
        if len(list) != 0:
            return str(list[0])
        else:
            return ''

    def insert_database(self, name, recipel, procedure, function, usage, source):
        try:
            self.cursor.execute("SELECT * FROM prescription WHERE name=%s", [name])
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        data = self.cursor.fetchone()
        if data is None:
            try:
                self.cursor.execute("INSERT INTO prescription VALUES(%s,%s,%s,%s,%s,%s)",
                                    [name, recipel, procedure, function, usage, source, ])
            except mysql.connector.Error as e:
                print('出错经方名：' + name + ' 出错原因：{}'.format(e))

    def parse(self, response):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        self.cursor = self.connection.cursor()

        urls = []
        count = 1
        for each in response.xpath('//*[@id="tab-content"]/li/a'):
            tmp_url = each.xpath("@href").extract()[0]
            urls.append("http://www.zysj.com.cn/" + tmp_url)
            count += 1
            if count > 500:
                break

        for each_url in urls:
            res = requests.get(each_url).text
            html = etree.HTML(res)

            name = html.xpath('//*[@id="content"]/h1/text()')
            name = self.format_value(name)
            recipel = html.xpath('//p[contains(@class,"cf")]/text()')
            recipel = self.format_value(recipel)
            procedure = html.xpath('//p[contains(@class,"zf")]/text()')
            procedure = self.format_value(procedure)
            function = html.xpath('//p[contains(@class,"gnzz")]/text()')
            function = self.format_value(function)
            usage = html.xpath('//p[contains(@class,"yfyl")]/text()')
            usage = self.format_value(usage)
            add = html.xpath('//*[@id="content"]/p[5]/text()')
            add = self.format_value(add)
            source = html.xpath('//p[contains(@class,"zl")]/text()')
            source = self.format_value(source)
            if add != source:
                usage += add

            self.insert_database(name, recipel, procedure, function, usage, source)
            self.connection.commit()

        # if self.page < self.maxpage:
        #     self.page += 1
        # else:
        #     self.connection.close()
        #     self.cursor.close()
        self.connection.close()
        self.cursor.close()
        # return scrapy.Request(self.url.format(str(self.page)), callback=self.parse)
