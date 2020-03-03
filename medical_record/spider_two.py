import requests
from lxml import etree
import re


# http://www.wfszyy.com/item-84-1655-1.html

def spider_two():
    response = requests.get("http://www.wfszyy.com/item-84-1655-1.html").text
    html = etree.HTML(response)
    text_list = html.xpath("/html/body/div[6]/div/div/div[1]/div[4]/div[2]/p//text()")

    count = 0
    while count < len(text_list):
        text_list[count] = str(text_list[count])
        # 去除\r\n
        text_list[count] = text_list[count].replace('\r\n', '')
        # 去除单独的\xa0
        if text_list[count] == "\xa0":
            text_list.pop(count)
        # 去除字符串中的\xa0
        elif "\xa0" in text_list[count]:
            text_list[count] = "".join((text_list[count].split()))
        else:
            count += 1

    text = "".join(text_list)

    # 按医案分割
    res = re.split(r"医案：?\d{1,2}", text)
    # 去除空格与最后一个缺失的医案
    res.pop(0)
    res.pop(len(res) - 1)
    res[39] = res[39] + "医案：1" + res[40]
    res.pop(40)
    # 去除按语部分
    for i in range(len(res)):
        pos = res[i].find("【按")
        res[i] = res[i][0:pos]

    return res


if __name__ == '__main__':
    spider_two()
