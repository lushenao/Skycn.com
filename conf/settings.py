#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

import os,pickle,sys,platform,shelve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)

'''
定义了mysql连接配置信息
'''
DATABASE_mysql = {
    'engine':'mysql',
    'host': '47.101.179.8',
    'port': 3306,
    'user': 'softsdown',
    'pwd': 'softsdown',
    'db': 'softsdown',
    'file_path': '%s/db' % BASE_DIR
}

