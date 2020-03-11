from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
browser.get('https://www.zk120.com/an/ks/%E7%94%B7%E7%A7%91?nav=ys')

# 登录
# browser.find_element_by_link_text("登录").click()
# browser.find_element_by_link_text("手机号登录").click()
# browser.find_element_by_class_name("pwd_login").click()
# browser.find_element_by_id("pwd_id_username").send_keys("13770690766")
# browser.find_element_by_id("pwd_id_passwod").send_keys("grxc12106abc123")
# browser.find_element_by_id("pwd_login_submit").click()

hyperlinks = browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
count = len(hyperlinks)
cur_linlk = 0
while cur_linlk < count:
    hyperlinks = browser.find_elements_by_xpath("//*[contains(@class,'cls_list')]/li/a")
    hyperlinks[cur_linlk].click()
    time.sleep(1)

    records = browser.find_elements_by_class_name('pb15')
    for record in records:
        source = record.find_element_by_class_name("resultItemTail").get_attribute("textContent")
        # 获取当前窗口
        current_window = browser.current_window_handle
        if "世中联名老中医典型医案" in source:
            record.click()
            handles = browser.window_handles
            browser.switch_to.window(handles[1])
            name = browser.find_element_by_tag_name('h2').get_attribute("textContent")
            print(name)
            text = browser.find_element_by_xpath(
                "//div[@class='detail_wrapper']/div[contains(@class,'space_pl')]").get_attribute("textContent")
            print(text)
            browser.close()
            browser.switch_to.window(current_window)
        break
    break

    # browser.back()
    # time.sleep(1)
    # cur_linlk += 1

browser.close()
