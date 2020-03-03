import requests
from lxml import etree
import re


# http://www.360doc.com/content/18/0508/13/1440676_752148679.shtml

def spider_one():
    response = requests.get("http://www.360doc.com/content/18/0508/13/1440676_752148679.shtml").text
    html = etree.HTML(response)
    result = html.xpath('//*[@id="artContent"]/div//text()')
    # result为列表 每一项类型为lxml.etree._ElementUnicodeResult
    text = "".join(result)

    # 修复不一致格式
    _list = list(text)
    _list.insert(_list.index('眩'), '.')
    text = "".join(_list)

    # 按每一项分割
    text_list = re.split("(\d{1,2}\.[^0-9])", text)

    # 去除连续\xa0
    for i in range(1, 83):
        tmp = list(text_list[i])
        count = 1
        while count < len(tmp):
            if tmp[count] == '\xa0' and tmp[count - 1] == '\xa0':
                tmp.pop(count)
            else:
                count = count + 1
        text_list[i] = "".join(tmp)

    for i in range(1, 82, 2):
        text_list[i] = text_list[i].replace(str(int((i + 1) / 2)) + ".", "")

    # 去除开头空格
    text_list.pop(0)

    res = []
    for i in range(0, len(text_list), 2):
        record = text_list[i] + text_list[i + 1]
        res.append(record)

    return res


if __name__ == '__main__':
    spider_one()
