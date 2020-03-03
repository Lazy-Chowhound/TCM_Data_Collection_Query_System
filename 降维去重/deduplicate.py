import mysql.connector
from SimHash import SimHash


class deduplicate:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.simHash = []

    def connect_database(self, user, password, database):
        try:
            self.connection = mysql.connector.connect(user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
        except mysql.connector.errors as e:
            print("ERROR!{}".format(e))

    def getTextSimHash(self):
        self.cursor.execute("SELECT * FROM medical_record")
        res = self.cursor.fetchall()
        for i in range(len(res)):
            sim = SimHash(str(res[i][0]))
            self.simHash.append(sim)
        return self.simHash
