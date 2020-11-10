def bytes_to_dic(dic):
    new_dic = dict()
    for i in dic.items():
        new_dic[i[0].decode("utf-8")] = int(i[1].decode("utf-8"))
    return new_dic