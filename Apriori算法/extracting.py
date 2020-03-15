import jieba.analyse
import re
import mysql.connector

"""
初步提取经方药材
"""


class extracting:
    connection = None
    cursor = None
    stop_words = ['片', ' ', ',', '，', '各', '两', 'g', '钱', '分', '、', '?', '。', '～', '；', '克', '个', '毫升', 'ml', '只', '枚',
                  '斤', '升', '握', '．', '各等分']

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
            self.cursor = self.connection.cursor()
        except mysql.connector.errors as e:
            print("ERROR!{}".format(e))

    def remove_useless(self, string):
        """
        简单地去除括号及其内容以及用量
        :param string:
        :return:
        """
        # 去除括号及其里面的内容
        s = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", string)
        s = re.sub(u"\d+\.{0,1}\d*", " ", s)
        return s

    def remove_stopwords(self, words):
        """
        去除停用词
        :param words:
        :return:
        """
        count = 0
        while count < len(words):
            if words[count] in self.stop_words:
                words.pop(count)
            else:
                count += 1
        return words

    def split_recipel(self, string):
        """
        去除空格 按照空格或中文逗号顿号分割
        :param string:
        :return:列表
        """
        # 去括号和句号
        s = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", string)
        s = s.replace("。", "")
        text = s.split(' ')
        if len(text) == 1:
            text = text[0]
        else:
            return text

        text = s.split('，')
        if len(text) == 1:
            text = text[0]
        else:
            return text

        text = s.split('、')
        if len(text) == 1:
            text = text[0]
        else:
            return text

        return [text]

    def remove_digit(self, textlist):
        count = 0
        while count < len(textlist):
            numlist = re.search('\d+', textlist[count])
            if numlist is not None:
                numlist = numlist.group()
                firstnum = numlist[0]
                pos = textlist[count].index(firstnum)
                textlist[count] = textlist[count][0:pos]
            count += 1
        return textlist

    def extract_drug(self, string):
        """
        最优提取经方中的药材
        :return:
        """
        raw_drug = string
        raw_drug2 = raw_drug[:]

        drugs = self.remove_useless(raw_drug)
        drugs = jieba.cut(drugs, cut_all=False, HMM=True)
        drugs = self.remove_stopwords(list(drugs))

        for drug in drugs:
            if len(drug) == 1:
                drugs = self.split_recipel(raw_drug2)
                drugs = self.remove_digit(drugs)
                break

        drug = "/".join(drugs)

        return drug

    def extract_all(self):
        self.cursor.execute('SELECT * FROM prescription')
        jieba.load_userdict('中药材词库.txt')
        for item in self.cursor.fetchall():
            name = str(item[0])
            raw_drug = str(item[1])

            drug = self.extract_drug(raw_drug)

            self.cursor.execute("UPDATE prescription SET drug=%s WHERE name=%s", [drug, name, ])
            self.connection.commit()


if __name__ == '__main__':
    extract = extracting()
    # numbering.extract_all()
