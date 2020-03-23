import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import calinski_harabasz_score


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

    def clusterResult(self):
        """
        聚类结果
        :return:
        """
        statistics = {}
        for i in range(self.category):
            statistics[i] = 0
        for each in self.kMeansModel.labels_:
            statistics[each] += 1
        print(statistics)

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


if __name__ == '__main__':
    cluster = Cluster()
    cluster.readData()
    cluster.dataStandardization()
    cluster.reduceDimension(2)
    cluster.kMeans(7)
    cluster.clusterResult()
    cluster.drawGraph()
