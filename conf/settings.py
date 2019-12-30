#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

soft_desc = {
    '`soft_size`':'',
    '`soft_version`':'',
    '`soft_update_time`':'',
    '`soft_operating_system_bit`':'',
    '`soft_language`':'',
    '`soft_auth`':'',
    '`soft_operating_system`':'',
    '`soft_comment`':''
}

