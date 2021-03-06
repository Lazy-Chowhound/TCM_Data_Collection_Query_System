from numpy import *
import MedicineList
from time import time

"""
Apriori算法
"""


# 构造数据
def loadDataSet():
    return MedicineList.pres_medicine


def createC1(dataSet):
    """
    将所有元素转换为frozenset型字典，存放到列表中
    :param dataSet:
    :return: [frozenset({1}),frozenset({2}),...]
    """
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # 使用frozenset是为了后面可以将这些值作为字典的键
    return list(map(frozenset, C1))


def scanD(D, Ck, minSupport):
    """
    过滤掉不符合支持度的集合
    :param D:原始项集
    :param Ck:候选频繁项集 为frozenset
    :param minSupport:
    :return:频繁项集列表retList 单独frozenset值的支持度字典
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            # 判断can是否是tid的子集
            if can.issubset(tid):
                # 统计整个记录中满足出现的次数（以字典的形式记录，frozenset为键）
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    # 记录支持度大于阈值的数据值
    retList = []
    # 每个数据值的支持度
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):
    """
    [frozenset({2, 3}), frozenset({3, 5})] -> [frozenset({2, 3, 5})]
    :param Lk:频繁项集列表Lk
    :param k:项集元素个数k
    :return:返回候选频繁项集列表Ck
    """
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 每次比较两个list，如果相同则求并集得到k个元素的集合
            # k-2为前一个频繁项集每一项的最后一个元素所在位置
            # 如k=2时即求含两个元素的频繁项集 而此时前一个只含一个元素频繁项集只有0上有元素
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport):
    """
    所有满足大于阈值的组合
    :param dataSet:
    :param minSupport:
    :return: 集合支持度列表
    """
    D = list(map(set, dataSet))
    C1 = createC1(
        dataSet)
    # 去除小于最小支持度的项集
    L1, supportData = scanD(D, C1, minSupport)
    # L保存的是所有频繁项集 相同个数的项集为一个列表
    # 如 L=[[{1},{2}],[{1,2},{2,3}],...] L[0]为1个项的频繁项集列表
    L = [L1]
    # k代表当前欲求的频繁项集里元素的个数
    k = 2
    # k-2为前一个频繁项集
    while len(L[k - 2]) > 0:
        # Ck候选频繁项集
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf):
    """
    获取关联规则
    :param L:频繁项集列表
    :param supportData:频繁项集及其支持度字典
    :param minConf:最小置信度
    :return:
    """
    bigRuleList = []
    # 从为2个元素的频繁项集开始
    for i in range(1, len(L)):
        for freqSet in L[i]:
            # frozenset({2, 3}) 转换为 [frozenset({2}), frozenset({3})]
            H1 = [frozenset([item]) for item in freqSet]
            # 如果集合元素大于2个，则需要处理才能获得规则
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf):
    """
    对规则进行评估 获得满足最小置信度的关联规则
    :param freqSet:
    :param H:
    :param supportData:
    :param brl:
    :param minConf: 最小置信度
    :return:
    """
    prunedH = []
    for conseq in H:
        # conf{B}=sup{A,B}-sup{A}
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf):
    """
    生成候选规则集合
    :param freqSet:
    :param H:
    :param supportData:
    :param brl:
    :param minConf: 最小置信度
    :return:
    """
    m = len(H[0])
    # 尝试进一步合并
    if len(freqSet) > (m + 1):
        # 将单个集合元素两两合并
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        # 不止一条规则满足要求
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


if __name__ == '__main__':
    start = time()

    dataSet = loadDataSet()
    L, suppData = apriori(dataSet, minSupport=0.01)
    rules = generateRules(L, suppData, minConf=0.3)
    print(L)
    print(suppData)
    # print(rules)

    end = time()
    print("运行结束，共花费{}秒".format(int(end - start)))
