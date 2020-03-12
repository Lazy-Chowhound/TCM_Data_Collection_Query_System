# coding:utf-8
import json
import requests
import mysql.connector


class herbSpider:
    request_url = "https://www.zyctd.com/api/data-service/api/v1/product/getTcmEffect"
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.zyctd.com',
        'Origin': 'https://www.zyctd.com',
        'plat_id': '1001',
        'Referer': 'https://www.zyctd.com/data/ycgx.html?id=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36 '}

    connection = None
    cursor = None

    current_page = 1
    max_page = 1866

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        self.cursor = self.connection.cursor()

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

    def crawl_page(self, page):
        """
        爬取单独的药材
        :param page:
        :return:
        """
        payloadData = {
            "init": 0,
            "tcmId": str(page),
            "years": "0"
        }
        response = requests.post(self.request_url, data=json.dumps(payloadData), headers=self.headers)
        print("--------------正在爬取第{}个----------------".format(str(page)))
        json_dict = response.json()
        if json_dict['data'] is not None:
            name = json_dict['data']['tcmName'].strip()
            effect = json_dict['data']['indications'].strip()
            self.insert_database(name, effect)

    def start_crawl(self):
        while self.current_page <= self.max_page:
            self.crawl_page(self.current_page)
            self.current_page += 1
        print("--------------爬取结束----------------")

    def end_crawl(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    spider = herbSpider()
    spider.start_crawl()
    spider.end_crawl()
