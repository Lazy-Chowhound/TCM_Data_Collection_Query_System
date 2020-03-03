import requests
import re
from lxml import etree


# http://www.zysj.com.cn/mingyi/chensusheng/518-6-0.html

def spider_three():
    response = requests.get("http://www.zysj.com.cn/mingyi/chensusheng/518-6-0.html").text
    html = etree.HTML(response)
    text_list = html.xpath('//*[@id="content"]/p/text()|//*[@id="content"]/p/strong/text()')

    count = 0
    while count < len(text_list):
        text_list[count] = str(text_list[count])
        if text_list[count].startswith("按："):
            text_list.pop(count)
        else:
            count += 1

    text = "".join(text_list)
    # 按医案分割
    res = re.split("案[\u4e00-\u9fa5]{1,3}、", text)
    # 去除首个空格
    res.pop(0)
    res[1] = res[1].replace("懊（忄农）nao", "")

    return res


if __name__ == '__main__':
    spider_three()
