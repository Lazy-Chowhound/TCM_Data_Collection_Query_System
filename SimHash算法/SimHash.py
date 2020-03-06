import jieba.analyse
import numpy


class SimHash:
    def __init__(self, string):
        self.simHash = self.simhash(string)

    def __str__(self):
        return str(self.simHash)

    def getsimHash(self):
        return str(self.simHash)

    def hash_string(self, string):
        """
        未采用自带的hash函数
        :param source:
        :return:
        """
        x = ord(string[0]) << 7
        m = 1000003
        mask = 2 ** 128 - 1
        for c in string:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(string)
        if x == -1:
            x = -2
        x = bin(x).replace('0b', '').zfill(64)[-64:]
        return str(x)

    def simhash(self, string):
        # 分词
        jieba.load_userdict('medical.txt')
        jieba.analyse.set_stop_words('stop_words.txt')
        keyword = jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=())
        # 加权
        keyList = []
        for feature, weight in keyword:
            weight = int(weight * 20)
            feature = self.hash_string(feature)
            tmp = []
            for ch in feature:
                if ch == '1':
                    tmp.append(weight)
                else:
                    tmp.append(-weight)
            keyList.append(tmp)
        # 合并
        res = numpy.sum(numpy.array(keyList), axis=0)
        # 降维
        sim_hash = ''
        for each in res:
            if each > 0:
                sim_hash = sim_hash + '1'
            else:
                sim_hash = sim_hash + '0'
        return sim_hash

    def hammingDistance(self, sim):
        """
        计算汉明距离
        :param sim: SimHash对象
        :return:
        """
        hash1 = '0b' + str(self.simHash)
        hash2 = '0b' + str(sim.simHash)
        # 异或求1的个数
        num = int(hash1, 2) ^ int(hash2, 2)
        dis = 0
        while num > 0:
            num = num & (num - 1)
            dis = dis + 1
        return dis


if __name__ == '__main__':
    sim1 = SimHash("你妈妈喊你回家吃饭哦，回家咯回家咯")
    print(sim1)
    sim2 = SimHash("你爸爸喊你回家学习，快回家快回家")
    print(sim2)
    print(sim1.hammingDistance(sim2))
