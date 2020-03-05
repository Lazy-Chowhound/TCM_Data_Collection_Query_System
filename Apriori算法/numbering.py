import mysql.connector


class numbering:
    connection = None
    cursor = None
    # 所有药材列表
    medicine = None
    # 每一经方药材列表
    pres_medicine = []

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
            self.cursor = self.connection.cursor()
        except mysql.connector.errors as e:
            print("ERROR!{}".format(e))

    def listing(self):
        """
        所有药材列表
        :return: 编号字典
        """
        self.cursor.execute("SELECT * FROM prescription")
        # 药材集合
        medi_set = set()
        for item in self.cursor.fetchall():
            drugs = str(item[6])
            medi_list = drugs.split('/')
            # 求并集
            medi_set = medi_set | set(medi_list)
        self.medicine = list(medi_set)

    def number(self):
        """
        将每一种经方的药材转化为编号
        :return:
        """
        self.cursor.execute("SELECT * FROM prescription")
        for item in self.cursor.fetchall():
            drugs = str(item[6])
            medi = []
            medi_list = drugs.split('/')
            for each in medi_list:
                medi.append(self.medicine.index(each))
            self.pres_medicine.append(medi)


if __name__ == '__main__':
    numbering = numbering()
    numbering.listing()
    numbering.number()
    print(numbering.medicine)
    print(numbering.pres_medicine)
