#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

def dicttomysqlupdate(dict,dict_len):
    keys = list(dict.keys())
    # print(keys)
    value = list(dict.values())
    # print(value)
    new = []
    for i in range(dict_len):
        a = '%s=%s' % (str(keys[i]), str(value[i]))
        new.append(a)
    new = ','.join(new)
    return new
