# -*- coding: utf-8 -*-
import scrapy
import mysql.connector


class HerbSpiderSpider(scrapy.Spider):
    name = 'herb_spider'
    # allowed_domains = ['https://www.zyctd.com/data/ycgx.html']
    start_urls = []
    url = ""

    starting_page = None
    max_page = None
    start_urls.append(url.format(str(starting_page)))

    connection = None
    cursor = None

    def insert_database(self, name, effect):
        """
        将数据插入数据库
        :param name:
        :param effect:
        :return:
        """
        try:
            self.cursor.execute("SELECT * FROM herb WHERE name=%s", [name])
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        data = self.cursor.fetchone()
        if data is None:
            try:
                self.cursor.execute("INSERT INTO herb VALUES(%s,%s)", [name, effect, ])
                self.connection.commit()
            except mysql.connector.Error as e:
                print('insert fails!{}'.format(e))

    def parse(self, response):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        self.cursor = self.connection.cursor()

        if self.starting_page < 1:
            self.starting_page += 1
        else:
            self.connection.close()
            self.cursor.close()

        return scrapy.Request(self.url.format(str(self.starting_page)), callback=self.parse)
