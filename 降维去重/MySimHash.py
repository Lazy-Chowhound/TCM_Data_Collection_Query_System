# 字符串哈希值
def hash_string(string):
    """
    字符串转hash值
    :param string: 原始字符串
    :return:
    """
    # 使用自带的hash函数
    decimal_hash = hash(string)
    binary_hash = bin(decimal_hash)
    if decimal_hash < 0:
        binary_hash = binary_hash[3:]
        binary_hash = "1" + binary_hash
    else:
        binary_hash = binary_hash[2:]
        binary_hash = "0" + binary_hash
    return binary_hash


# 加权
def simhash_string(hash_string, weight):
    """
    根据hash值求simhash值
    :param hash_string: 哈希值字符串
    :param weight:
    :return:
    """
    weight = round(weight * 10)
    simhash_str = []
    for i in range(len(hash_string)):
        num = int(hash_string[i])
        if num == 1:
            simhash_str.append(str(weight))
        else:
            simhash_str.append(str(-weight))
    return simhash_str


def SimHash(raw_list):
    """
    根据分词结果求字符串simhash
    :param raw_list: 关键词列表
    :return:
    """
    max_length = 0
    res = []
    for i in range(len(raw_list)):
        re = []
        hash_s = hash_string(raw_list[i][0])
        re.append(hash_s)
        re.append(raw_list[i][1])
        max_length = max(len(hash_s), max_length)
        res.append(re)

    # 补0
    i = 0
    for i in range(len(res)):
        length = len(res[i][0])
        if length < max_length:
            j = 0
            for j in range(max_length - length):
                res[i][0] = "0" + res[i][0]

    # 加权
    for i in range(len(res)):
        res[i] = simhash_string(res[i][0], res[i][1])

    # 合并降维
    final = ""
    for i in range(max_length):
        each = 0
        for j in range(len(res)):
            each += int(res[j][i])
        if each > 0:
            final += "1"
        else:
            final += "0"

    return final
