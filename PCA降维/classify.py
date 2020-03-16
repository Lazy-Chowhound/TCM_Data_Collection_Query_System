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
        for i in range(1, len(modifier.rows)):
            for j in range(2, len(modifier.rows[0])):
                self.rows[i].append(0)

    def get_rows(self):
        for row in self.rows:
            print(row)

    def set(self, row, column, num=1):
        self.rows[row][column] = num


if __name__ == '__main__':
    modifier = ModifyCsv('herb.csv', 'herb_ex.csv')
    modifier.read_csv()

    modifier.write_csv()
