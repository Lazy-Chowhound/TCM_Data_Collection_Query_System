# coding:utf-8
import csv
import os
import mysql.connector


class toCsv:
    csvfilePath = "herb.csv"

    connection = None
    cursor = None

    def __init__(self):
        # 如果存在该文件，则删除之前的
        if os.path.exists(self.csvfilePath):
            os.remove(self.csvfilePath)
        # 重新创建
        f = open(self.csvfilePath, "w+", encoding='utf8')
        f.close()
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        self.cursor = self.connection.cursor()

    def writeCsv(self):
        csvfile = open(self.csvfilePath, 'w', newline="", encoding='utf-8-sig')
        writer = csv.writer(csvfile)

        # 写入标题头
        writer.writerow(["名称", "功效"])

        self.cursor.execute("SELECT * FROM herb")
        result = self.cursor.fetchall()
        for res in result:
            name = res[0].encode("utf-8").decode('utf8')
            effect = res[1].encode("utf-8").decode('utf8')
            writer.writerow([name, effect])
        csvfile.close()


if __name__ == '__main__':
    to_csv = toCsv()
    to_csv.writeCsv()
