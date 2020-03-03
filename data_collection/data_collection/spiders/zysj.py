# -*- coding: utf-8 -*-
import scrapy
import mysql.connector
import requests
from lxml import etree


class zysjSpider(scrapy.Spider):
    name = 'zysjSpider'
    # allowed_domains = ['example.com']
    start_urls = ['http://www.zysj.com.cn/yianxinde/index1.html']
    url = "http://www.zysj.com.cn/yianxinde/index{0}.html"

    # 当前页码和最大页码
    page = 1
    maxpage = 10

    connection = None
    cursor = None

    def parse(self, response):
        self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        self.cursor = self.connection.cursor()

        # 本页的所有医案url
        urls = []
        for each in response.xpath('//*[@id="content"]/ul/li/a'):
            tmp_url = each.xpath('@href').extract()[0]
            urls.append("http://www.zysj.com.cn/" + tmp_url)

        # 保存所有医案
        record = []
        for tmp_url in urls:
            resp = requests.get(tmp_url).text
            html = etree.HTML(resp)
            text = html.xpath('//*[@id="content"]/p/text()')
            count = 0
            while count < len(text):
                text[count] = str(text[count])
                if text[count] == '\n' or text[count].startswith('□'):
                    text.pop(count)
                else:
                    count += 1
            record.append(''.join(text))

        for item in record:
            self.cursor.execute("SELECT * FROM medical_record WHERE record=%s", [item])
            data = self.cursor.fetchone()
            if data is None:
                self.cursor.execute(
                    "INSERT INTO medical_record VALUES(%s)",
                    [item, ])

            self.connection.commit()

        if self.page < self.maxpage:
            self.page = self.page + 1
        else:
            self.connection.close()
            self.cursor.close()
        return scrapy.Request(self.url.format(str(self.page)), callback=self.parse)
