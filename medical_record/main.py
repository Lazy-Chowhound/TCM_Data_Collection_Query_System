import mysql.connector

import spider_one
import spider_three
import spider_two

if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    cursor = connection.cursor()
    res1 = spider_one.spider_one()
    res2 = spider_two.spider_two()
    res3 = spider_three.spider_three()
    res = res1 + res2 + res3
    for item in res:
        try:
            cursor.execute("SELECT * FROM medical_record WHERE record=%s", [item])
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))
        data = cursor.fetchone()
        if data is None:
            try:
                cursor.execute(
                    "INSERT INTO medical_record VALUES(%s)",
                    [item, ])
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))

    connection.commit()
    cursor.close()
    connection.close()
