from selenium import webdriver
import time
import mysql.connector


class recordSpider:
    chrome_driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    browser = None
    urls = ['https://www.zk120.com/an/ks/眼科?nav=ys', ]

    connection = None
    cursor = None

    def __init__(self):
        self.browser = webdriver.Chrome(
            executable_path=self.chrome_driver_path)
        # 隐式等待5s
        self.browser.implicitly_wait(5)
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        self.cursor = self.connection.cursor()

    def login(self):
        """
        登录
        :return:
        """
        self.browser.get("https://www.zk120.com/?nav=ys")
        self.browser.find_element_by_link_text("登录").click()
        self.browser.find_element_by_link_text("手机号登录").click()
        self.browser.find_element_by_class_name("pwd_login").click()
        self.browser.find_element_by_id("pwd_id_username").send_keys("13770690766")
        self.browser.find_element_by_id("pwd_id_passwod").send_keys("grxc12106abc123")
        self.browser.find_element_by_id("pwd_login_submit").click()

    def insert_database(self, name, text):
        """
        数据插入数据库
        :param name:
        :param text:
        :return:
        """
        try:
            self.cursor.execute("SELECT * FROM medical_record WHERE name=%s", [name])
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        data = self.cursor.fetchone()
        if data is None:
            try:
                self.cursor.execute("INSERT INTO medical_record VALUES(%s,%s)", [name, text, ])
                self.connection.commit()
            except mysql.connector.Error as e:
                print('{}insert fails!{}'.format(name, e))

    def crawl_page(self):
        """
        爬取每一页
        :return:
        """
        hyperlinks = self.browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
        count = len(hyperlinks)
        print("共{}个病症".format(count))
        cur_link = 0
        while cur_link < count:
            # 点击每一个病症
            hyperlinks = self.browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
            # 病症名
            name = hyperlinks[cur_link].get_attribute("textContent")
            hyperlinks[cur_link].click()
            time.sleep(0.5)
            # 获取医案列表
            records = self.browser.find_elements_by_class_name('pb15')
            for record in records:
                # 获取当前窗口
                current_window = self.browser.current_window_handle
                source = record.find_element_by_class_name("resultItemTail").get_attribute("textContent")
                time.sleep(0.5)
                if "世中联名老中医典型医案" in source or "中医男科名家验案精选" in source:
                    record.click()
                    time.sleep(0.5)
                    handles = self.browser.window_handles
                    self.browser.switch_to.window(handles[1])
                    text = self.browser.find_elements_by_xpath(
                        "//div[@class='detail_wrapper']/div[contains(@class,'space_pl')]/p")
                    content = ""
                    for each in text:
                        content += each.get_attribute("textContent").strip() + " "

                    mt = self.browser.find_elements_by_xpath(
                        "//div[@class='detail_wrapper']/div[contains(@class,'space_pl')]/div[@class='mt10']/p")
                    for each in mt:
                        content += each.get_attribute("textContent").strip() + " "
                    self.insert_database(name, content)
                    # 关闭打开的医案新页面
                    self.browser.close()
                    # 回到医案列表页面
                    self.browser.switch_to.window(current_window)
                    break
            # 回到病症页面
            self.browser.back()
            cur_link += 1

    def start_crawl(self):
        for url in self.urls:
            self.browser.get(url)
            self.crawl_page()

    def end_crawl(self):
        self.browser.close()
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    spider = recordSpider()
    spider.login()
    spider.start_crawl()
    spider.end_crawl()
