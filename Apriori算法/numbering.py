import jieba.analyse
import re


def remove_useless(string):
    """
    简单地去除括号及其内容以及用量
    :param string:
    :return:
    """
    s = string.replace("克", "")
    # 去除括号及其里面的内容
    s = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", s)
    s = re.sub(u"\d+\.{0,1}\d*", " ", s)
    return s


def remove_stopwords(words):
    """
    去除停用词
    :param words:
    :return:
    """
    stop_words = ['片', ' ', ',']
    count = 0
    while count < len(words):
        if words[count] in stop_words:
            words.pop(count)
        else:
            count += 1
    return words


if __name__ == '__main__':
    s = "白术3克（炒）,云苓3克 蔻米1.5克（研）法夏3克 扁豆9克（炒）制草1.5克 煨姜1片 伏龙肝3克"
    s = remove_useless(s)

    jieba.load_userdict('中药材词库.txt')
    words = jieba.cut(s, cut_all=False, HMM=True)
    words = list(words)

    print(remove_stopwords(words))
