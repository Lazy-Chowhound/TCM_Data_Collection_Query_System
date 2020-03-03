import pypinyin


# 将多个txt整合到一起

def integrate(file, res):
    for line in file.readlines():
        if line not in res:
            res.append(line)


def sort_pinyin(hanzi_list):
    hanzi_list_pinyin = []
    hanzi_list_pinyin_alias_dict = {}
    for single_str in hanzi_list:
        py_r = pypinyin.lazy_pinyin(single_str)
        single_str_py = ''
        for py_list in py_r:
            single_str_py = single_str_py + py_list
        hanzi_list_pinyin.append(single_str_py)
        hanzi_list_pinyin_alias_dict[single_str_py] = single_str
    hanzi_list_pinyin.sort()
    sorted_hanzi_list = []
    for single_str_py in hanzi_list_pinyin:
        sorted_hanzi_list.append(hanzi_list_pinyin_alias_dict[single_str_py])
    return sorted_hanzi_list


if __name__ == '__main__':
    file1 = open("1.txt", encoding='utf8')
    file2 = open("2.txt", encoding='utf8')
    file3 = open("3.txt", encoding='utf8')
    file4 = open("4.txt", encoding='utf8')
    file5 = open("5.txt", encoding='utf8')

    res = []
    integrate(file1, res)
    integrate(file2, res)
    integrate(file3, res)
    integrate(file4, res)
    integrate(file5, res)

    result = sort_pinyin(res)

    ffile = open("medical.txt", 'w')
    for item in result:
        ffile.write(item)
    ffile.close()
    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()
