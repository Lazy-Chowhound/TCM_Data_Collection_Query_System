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

    def reduceDimension(self):
        """
        PCA降维
        :return:
        """
        pca = PCA(n_components=2)
        self.newX = pca.fit_transform(self.standardX)
        print(pca.explained_variance_ratio_)
        # count = 0
        # for each in pca.explained_variance_ratio_:
        #     count += each
        # print(count)

    def kMeans(self, kind):
        self.kMeansModel = KMeans(n_clusters=kind, max_iter=300).fit(self.newX)
        score = calinski_harabasz_score(self.newX, self.kMeansModel.labels_)
        # 评价标准之一calinski_harabasz分数 越大越好
        print("聚类{}簇的calinski_harabasz分数为".format(str(score)))

    def drawGraph(self, kind):
        plt.figure(figsize=(10, 10))
        colors = ['g', 'r', 'y', 'b', 'darkorange', 'indigo', 'cyan', 'peru', 'darkcyan', 'darkmagenta', 'gray',
                  'yellow']
        markers = ['o', 's', 'd', 'h']
        statistics = {}
        for i in range(kind):
            statistics[i] = 0
        for i, l in enumerate(self.kMeansModel.labels_):
            plt.plot(self.newX[i][0], self.newX[i][1], color=colors[l], marker=markers[1], ls='None')
            statistics[l] += 1
        print(statistics)
        # 簇中心点

        plt.title("Medicine Categories")
        plt.show()


if __name__ == '__main__':
    cluster = Cluster()
    cluster.readData()
    cluster.dataStandardization()
    cluster.reduceDimension()
    cluster.drawGraph(12)
