import jieba
import jieba.analyse


def apart(words, stop_words):
    words = list(words)
    i = 0
    while i < len(words):
        if words[i] == ' ' or words[i] == '\xa0':
            words.pop(i)
        elif words[i] in stop_words:
            words.pop(i)
        else:
            i += 1
    return words


s2 = '蒋×  女  17岁患全身性红斑狼疮2年，心、肝、脾、肾均有不同程度损害，长期应用大剂量地塞米松治疗，激素撤减困难。面如满月，颞颐痤疮累' \
     '累，毛发稀疏，身热颧红，肝区胀痛，四肢关节红肿痛楚。舌质红、苔薄白、脉弦。证属肝郁凝瘀成毒，阴虚火旺营热。先生予疏肝和络、清化' \
     '解毒之剂；重用土茯苓、忍冬藤各30g  连翘、白薇各9g。连服2月后，诸恙渐平。追踪1年症情稳定。'

# jieba.load_userdict('medical.txt')
# jieba.analyse.set_stop_words('stop_words.txt')
# words = jieba.cut(s2, cut_all=False, HMM=True)

# stop_words = []
# file = open('stop_words.txt', encoding='utf8')
# for item in file.readlines():
#     stop_words.append(item.strip())
#
# words = apart(words, stop_words)
# print(words)

# list = jieba.analyse.extract_tags(s2, topK=20, withWeight=True)
# print(list)
#
#
# list2 = jieba.analyse.textrank(s2, withWeight=True)
# print(list2)
