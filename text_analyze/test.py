# coding:utf-8
import csv
import os

import mysql.connector

"""
将数据库数据转换为.csv文件
"""


class toCsv:
    csvfilePath = ""

    connection = None
    cursor = None

    def __init__(self, filePath):
        # 如果存在该文件，则删除之前的
        self.csvfilePath = filePath
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
        writer.writerow(["名称", "记录", "诊断", "用药与病情变化"])

        self.cursor.execute("SELECT * FROM medical_info.medical_record")
        result = self.cursor.fetchall()
        for res in result:
            name = res[0].encode("utf-8").decode('utf8')
            record = res[1].encode("utf-8").decode('utf8')
            diagnose = res[2].encode("utf-8").decode('utf8')
            illness = res[3].encode("utf-8").decode('utf8')
            writer.writerow([name, record, diagnose, illness])
        csvfile.close()


if __name__ == '__main__':
    to_csv = toCsv("record.csv")
    to_csv.writeCsv()
