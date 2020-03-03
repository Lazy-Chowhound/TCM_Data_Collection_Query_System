import jieba
import jieba.analyse
import re


def remove_useless(string):
    """
    去除括号和一些停用词
    :param string:
    :return:
    """
    s = string.replace("克", "")
    # 去除括号及其里面的内容
    s = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", s)
    s = re.sub(u"\d+\.{0,1}\d*", " ", s)
    return s


if __name__ == '__main__':
    dict = {'A': 1}
    s = "白术3克（炒）,云苓3克 蔻米1.5克（研）法夏3克 扁豆9克（炒）制草1.5克 煨姜1片 伏龙肝3克"
    s = remove_useless(s)

    jieba.load_userdict('medical.txt')
    jieba.analyse.set_stop_words('stop_words.txt')
    words = jieba.cut(s, cut_all=False, HMM=True)
    print("/".join(words))
