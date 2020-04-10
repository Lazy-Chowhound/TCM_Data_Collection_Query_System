import csv

import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import calinski_harabasz_score
from sklearn.preprocessing import StandardScaler


class Cluster:
    X = None
    standardX = None
    newX = None
    kMeansModel = None
    category = 0

    def readData(self):
        source_file = open("herbData.csv", "r", encoding="utf-8-sig")
        reader = csv.reader(source_file)
        rows = []
        for row in reader:
            rows.append(row)
        source_file.close()
        self.X = np.array(rows)

    def dataStandardization(self):
        """
        数据标准化
        :return:
        """
        scaler = StandardScaler()
        self.standardX = scaler.fit_transform(self.X)

    def reduceDimension(self, dimension):
        """
        PCA降维
        :return:
        """
        pca = PCA(n_components=dimension)
        self.newX = pca.fit_transform(self.standardX)
        print("降为{}维后各维度占比{}".format(dimension, pca.explained_variance_ratio_))
        total = 0
        for each in pca.explained_variance_ratio_:
            total += each
        print("降为{}维后维度总占比{}".format(dimension, total))

    def kMeans(self, category):
        """
        KMeans聚类
        :param category:
        :return:
        """
        self.category = category
        self.kMeansModel = KMeans(n_clusters=category, max_iter=300).fit(self.newX)
        score = calinski_harabasz_score(self.newX, self.kMeansModel.labels_)
        # 评价标准之一calinski_harabasz分数 越大越好
        print("聚类{}簇的calinski_harabasz分数为{}".format(category, str(score)))

    def clusterResult(self, showAll):
        """
        聚类结果
        :return:
        """
        statistics = {}
        for i in range(self.category):
            statistics[i] = 0
        categoryList = self.kMeansModel.labels_
        for each in categoryList:
            statistics[each] += 1
        print(statistics)
        if showAll is True:
            print(categoryList)

    def drawGraph(self):
        """
        维度为2时可视化
        :return:
        """
        plt.figure(figsize=(10, 10))
        colors = ['grey', 'red', 'peru', 'gold', 'olivedrab', 'steelblue', 'slateblue', 'blueviolet']
        markers = ['o', 's', 'd', 'h', 'p', '^', 'v', '.']

        for i, l in enumerate(self.kMeansModel.labels_):
            plt.plot(self.newX[i][0], self.newX[i][1], color=colors[l], marker=markers[l], ls='None')

        # 每个簇类的中心点
        count = 0
        for point in self.kMeansModel.cluster_centers_:
            plt.plot(point[0], point[1], color=colors[count], marker='x', ls='None', markersize=12)
            count += 1

        plt.title("kMeans")
        plt.show()

    def markHerb(self):
        """
        聚类结果写入数据库
        :return:
        """
        connection = mysql.connector.connect(user="root", password="061210", database="medical_info")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM medical_info.herb")
        res = cursor.fetchall()
        name = []
        for each in res:
            name.append(each[0])
        count = 0
        for each in self.kMeansModel.labels_:
            cursor.execute("UPDATE medical_info.herb SET category=%s WHERE name=%s", [str(each), name[count]])
            count += 1
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    dimension = 12
    category = 7

    cluster = Cluster()
    cluster.readData()
    cluster.dataStandardization()
    cluster.reduceDimension(dimension)
    cluster.kMeans(category)
    cluster.clusterResult(showAll=False)
    if dimension == 2:
        cluster.drawGraph()
    cluster.markHerb()
