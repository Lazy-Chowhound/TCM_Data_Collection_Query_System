import mysql.connector


class Filter:
    connection = None
    cursor = None
    filt_words = ['、', ]

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
            drug = item[6]
            if '各' in drug:
                print(count)
            count += 1


if __name__ == '__main__':
    filter = Filter()
    filter.filt()
