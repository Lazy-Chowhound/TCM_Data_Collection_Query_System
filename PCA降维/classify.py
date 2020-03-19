# coding:utf-8
import csv


class ModifyCsv:
    rows = []
    reader = None
    writer = None

    def __init__(self, source, target):
        source_file = open(source, "r", encoding="utf-8-sig")
        self.reader = csv.reader(source_file)
        target_file = open(target, "w", encoding="utf-8-sig", newline="")
        self.writer = csv.writer(target_file)

    def read_csv(self):
        for row in self.reader:
            self.rows.append(row)

    def write_csv(self):
        for row in self.rows:
            self.writer.writerow(row)

    def initCsv(self):
        """
        添加新列
        :return:
        """
        headers = ['消食', '清热解表', '清热解毒', '温里', '理气', '驱虫泻下', '化痰止咳', '活血化瘀', '止血', '祛湿']
        for header in headers:
            self.rows[0].append(header)
        for i in range(1, len(self.rows)):
            for j in range(2, len(self.rows[0])):
                self.rows[i].append(0)

    def filter_symptom(self, symptom, column):
        count = 0
        for i in range(1, len(self.rows)):
            if symptom in self.rows[i][1]:
                if self.rows[i][column] != "1":
                    self.rows[i][column] = 1
                    count += 1
                    print(self.rows[i][0])
        print("改变了{}项".format(count))

    def get_rows(self):
        for row in self.rows:
            print(row)

    def set(self, name, columns, num=1):
        """
        将药材的某一列设为1或0
        :param name:
        :param column:
        :param num:
        :return:
        """
        items = name.split("、")
        count = 0
        for item in items:
            for i in range(1, len(self.rows)):
                if self.rows[i][0] == item:
                    for column in columns:
                        if self.rows[i][column] != str(num):
                            count += 1
                        self.rows[i][column] = num
        print("改变了{}项".format(count))

    def filt_untouched(self):
        for row in range(1, len(self.rows)):
            flag = 0
            for col in range(2, 13):
                if self.rows[row][col] == "1":
                    flag += 1
            if flag <= 0:
                print(self.rows[row][0])


if __name__ == '__main__':
    # 操作
    modifier = ModifyCsv('herb.csv', 'herb_ex.csv')
    modifier.read_csv()

    # modifier.filt_untouched()
    # 消食-2 清热解表-3 解毒排毒-4 温里-5 理气-6 驱虫泻下-7
    # 化痰止咳-8 活血化瘀-9 止血镇痛-10 祛湿-11 安神补益-12

    # modifier.filter_symptom("", 5)
    # modifier.filter_symptom("", 6)


    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)
    # modifier.set("", [], 1)

    modifier.write_csv()
