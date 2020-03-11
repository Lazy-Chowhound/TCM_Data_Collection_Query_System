from selenium import webdriver
import time


class recordSpider:
    chrome_driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    browser = None
    urls = ['https://www.zk120.com/an/ks/%E7%94%B7%E7%A7%91?nav=ys']

    def __init__(self):
        self.browser = webdriver.Chrome(
            executable_path=self.chrome_driver_path)

    def login(self):
        """
        登录
        :return:
        """
        self.browser.find_element_by_link_text("登录").click()
        self.browser.find_element_by_link_text("手机号登录").click()
        self.browser.find_element_by_class_name("pwd_login").click()
        self.browser.find_element_by_id("pwd_id_username").send_keys("13770690766")
        self.browser.find_element_by_id("pwd_id_passwod").send_keys("grxc12106abc123")
        self.browser.find_element_by_id("pwd_login_submit").click()

    def crawl_page(self):
        """
        爬取每一页
        :return:
        """
        hyperlinks = self.browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
        count = len(hyperlinks)
        cur_linlk = 0
        while cur_linlk < count:
            hyperlinks = self.browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
            hyperlinks[cur_linlk].click()
            time.sleep(3)

            records = self.browser.find_elements_by_class_name('pb15')
            for record in records:
                # 获取当前窗口
                current_window = self.browser.current_window_handle
                source = record.find_element_by_class_name("resultItemTail").get_attribute("textContent")
                if "世中联名老中医典型医案" in source or "中医男科名家精选" in source:
                    record.click()
                    handles = self.browser.window_handles
                    self.browser.switch_to.window(handles[1])
                    name = self.browser.find_element_by_tag_name('h2').get_attribute("textContent")
                    print(name)
                    text = self.browser.find_elements_by_xpath(
                        "//div[@class='detail_wrapper']/div[contains(@class,'space_pl')]/p")
                    string = ""
                    for i in text:
                        string += i.get_attribute("textContent").strip() + " "
                    print(string)
                    self.browser.close()
                    self.browser.switch_to.window(current_window)
                    break

            self.browser.back()
            cur_linlk += 1

    def start_crawl(self):
        for url in self.urls:
            self.browser.get(url)
            self.crawl_page()

    def end_crawl(self):
        self.browser.close()


if __name__ == '__main__':
    spider = recordSpider()
    spider.start_crawl()
    spider.end_crawl()
