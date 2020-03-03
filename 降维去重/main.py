from deduplicate import deduplicate
from time import time

start = time()

dedupli = deduplicate()
dedupli.connect_database('root', '061210', 'medical_info')
simHash = dedupli.getTextSimHash()
i = 0
while i < len(simHash):
    j = i + 1
    flag = 0
    while j < len(simHash):
        if simHash[i].hammingDistance(simHash[j]) < 3:
            flag = 1
            print("第{}个病案和第{}相似".format(i, j))
        j = j + 1
    i = i + 1
    if flag == 0:
        print("没有与第{}个病案相似的病案".format(i))

end = time()
print("检索结束，共花费{}秒".format(int(end - start)))
