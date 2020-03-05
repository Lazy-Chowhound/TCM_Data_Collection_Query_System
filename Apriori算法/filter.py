import mysql.connector


class Filter:
    connection = None
    cursor = None
    filt_words = ['各', '半', '钱', '适量', '分', '少', '许', '斤', '两']

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
            self.cursor = self.connection.cursor()
        except mysql.connector.errors as e:
            print("ERROR!{}".format(e))

    def filt(self):
        self.cursor.execute('SELECT * FROM prescription')
        count = 1
        for item in self.cursor.fetchall():
            drug = str(item[6])
            name = str(item[0])
            if '半两' in drug:
                drug = drug.replace("半两", "")
            if '半钱' in drug:
                drug = drug.replace("半钱", "")
            if '、' in drug:
                drug = drug.replace('、', '/')
            if '/钱半' in drug:
                drug = drug.replace('/钱半', '')
            if '各' in drug:
                drug = drug.replace('各', '')
            if '//' in drug:
                drug = drug.replace('//', '/')
            for word in self.filt_words:
                if word in drug:
                    print(count)
                    break
            self.cursor.execute("UPDATE prescription SET drug=%s WHERE name=%s", [drug, name, ])
            self.connection.commit()
            count += 1

    def is_split(self):
        self.cursor.execute('SELECT * FROM prescription')
        count = 1
        for item in self.cursor.fetchall():
            drug = str(item[6])
            # 判断是否有未分割的药材
            split_drug = drug.split("/")
            for each in split_drug:
                if len(each) == 4:
                    print(count)
                    break
            count += 1


if __name__ == '__main__':
    filter = Filter()
    filter.filt()
    filter.is_split()
