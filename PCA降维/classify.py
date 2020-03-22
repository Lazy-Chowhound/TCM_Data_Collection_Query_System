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

    def addColumn(self, name):
        """
        添加新列
        :return:
        """
        self.rows[0].append(name)
        for i in range(1, len(self.rows)):
            self.rows[i].append(0)

    def statistic(self):
        """
        筛选出药材功效的总数
        :return:
        """
        data = {}
        for i in range(1, 13):
            data[i] = 0
        for i in range(1, len(self.rows)):
            count = 0
            for j in range(2, 14):
                if self.rows[i][j] == "1":
                    count += 1
            data[count] += 1
        print(data)

    def filter_symptom(self, symptom, column):
        """
        将包含某个症状symptom的对应功效colummn设为1
        :param symptom:
        :param column:
        :return:
        """
        count = 0
        changed = []
        for i in range(1, len(self.rows)):
            if symptom in self.rows[i][1]:
                if self.rows[i][column] != "1":
                    self.rows[i][column] = 1
                    count += 1
                    changed.append(self.rows[i][0])
        print(changed)
        print("改变了{}项".format(count))

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

    def filter_untouched(self, limit):
        """
        筛选出功能数为limit的药材名
        :param limit:
        :return:
        """
        for row in range(1, len(self.rows)):
            flag = 0
            for col in range(2, 14):
                if self.rows[row][col] == "1":
                    flag += 1
            if flag <= limit:
                print(self.rows[row][0])

    def filter_column(self, column, option, except_words):
        """
        挑选出某个功效为0或1的药材行，不包括功效含except_words的药材
        :param column:
        :param option:
        :param except_words:
        :return:
        """
        string = ""
        word = except_words.split("、")
        i = 1
        while i < len(self.rows):
            flag = 0
            if self.rows[i][column] != str(option):
                flag = 1
            for each in word:
                if each in self.rows[i][1]:
                    flag = 1
                    break
            if flag == 1:
                del self.rows[i]
            else:
                i += 1

        for i in range(1, len(self.rows)):
            string += self.rows[i][0] + "、"
        print(string)

    def exportData(self):
        """
        导出数据
        :return:
        """
        del self.rows[0]
        for i in range(0, len(self.rows)):
            del self.rows[i][1]
            del self.rows[i][0]


if __name__ == '__main__':
    # 操作
    modifier = ModifyCsv('herb.csv', 'herb_ex.csv')
    modifier.read_csv()
    modifier.exportData()
    modifier.write_csv()
