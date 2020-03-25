# -*- coding: UTF-8 -*-
import mysql.connector
import time


class extract:
    connection = None
    cursor = None

    def __init__(self, user, password, database):
        try:
            self.connection = mysql.connector.connect(user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print("connect fails!{}'.format(e)")

    def insertToDatabase(self, name, diagnose, illness):
        try:
            self.cursor.execute(
                "UPDATE medical_info.medical_record SET ` diagnose` = %s,illnessInfo = %s WHERE name=%s",
                [diagnose, illness, name, ])
            self.connection.commit()
            print("-----{}完成-----".format(name))
        except mysql.connector.Error as e:
            print("insert fail!{}".format(e))

    def extractInfo(self, name, record):
        s = record[record.find('现病史'):]
        pos = s.find("治则治法")
        if pos == -1:
            pos = s.find("方名")
            if pos == -1:
                pos = s.find("方剂组成")
        if pos == -1:
            print("-----{}格式不同寻常，需单独处理-----".format(name))
            return
        diagnose = s[:pos]

        illness = s[pos:]
        illness = self.removeDate(illness)
        illness = self.removeNote(illness)
        self.insertToDatabase(name, diagnose, illness)

    def removeNote(self, string):
        pos = string.find("按语")
        while pos != -1:
            blank = string.find(" ", pos)
            string = string[:pos - 1] + string[blank:]
            pos = string.find("按语")
        return string

    def removeDate(self, string):
        pos = string.find("就诊时间")
        while pos != -1:
            blank = string.find(" ", pos)
            string = string[:pos - 1] + string[blank:]
            pos = string.find("就诊时间")
        return string

    def extractAll(self, begin, end):
        self.cursor.execute("SELECT * FROM medical_info.medical_record")
        res = self.cursor.fetchall()
        if end == '*':
            end = len(res)
        count = begin
        while count < end:
            name = res[count][0]
            record = res[count][1]
            self.extractInfo(name, record)
            count += 1

        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    ex = extract('root', '061210', 'medical_info')
    beg = time.time()

    ex.extractAll(500, "*")

    end = time.time()
    print("共花费{}秒".format(int(end - beg)))
