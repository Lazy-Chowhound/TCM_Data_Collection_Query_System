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

    def filter(self):
        for i in range(1, len(self.rows)):
            for j in range(2, len(self.rows[0])):
                if self.rows[0][j] in self.rows[i][1]:
                    self.rows[i][j] = 1
            if '解表' in self.rows[i][1]:
                self.rows[i][3] = 1
            if '解毒' in self.rows[i][1]:
                self.rows[i][4] = 1
            if '驱虫' in self.rows[i][1]:
                self.rows[i][7] = 1
            if '泻下' in self.rows[i][1]:
                self.rows[i][7] = 1
            if '祛痰' in self.rows[i][1]:
                self.rows[i][8] = 1
            if '化痰' in self.rows[i][1]:
                self.rows[i][8] = 1
            if '止咳' in self.rows[i][1]:
                self.rows[i][8] = 1
            if '活血' in self.rows[i][1]:
                self.rows[i][9] = 1
            if '化瘀' in self.rows[i][1]:
                self.rows[i][9] = 1
            if '健脾' in self.rows[i][1]:
                self.rows[i][10] = 1

    def filter_symptom(self, symptom, column):
        for i in range(1, len(self.rows)):
            if symptom in self.rows[i][1]:
                self.rows[i][column] = 1

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
                        if self.rows[i][column] != num:
                            count += 1
                        self.rows[i][column] = num
        print("改变了{}项".format(count))

    def filt_untouched(self):
        for row in range(1, len(self.rows)):
            flag = 0
            for col in range(2, 12):
                if self.rows[row][col] == "1":
                    flag += 1
            if flag <= 1:
                print(self.rows[row][0])


if __name__ == '__main__':
    # 操作
    modifier = ModifyCsv('herb.csv', 'herb_ex.csv')
    modifier.read_csv()

    # modifier.filt_untouched()

    modifier.write_csv()
