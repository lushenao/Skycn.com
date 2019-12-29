#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.skycn_com import Skycn_soft
#from src.soft_detailed_info import SoftDetailedInfo
from src.soft_detailed_info_multiThread import SoftDetailedInfo



class Start(object):
    '''
    start函数，输入关键字开始爬软件信息
    '''
    def run(self):
        exit_flag = False
        while True:
            title = '''\033[34;1m
--------------Skycn.com网站爬取工具--------------\033[0m
            '''
            print(title)
            search_name = input('\033[32;1m您想要搜索的软件关键字是？\n\033[37;1m(输入完毕请按回车,退出程序请输入Q)：\033[0m').strip()
            if len(search_name) == 0:
                print('\033[31;1m请输入关键字!')
                continue
            if search_name == 'Q':
                break
            #pages = input('\033[32;1m您想要爬取总页数？\n\033[37;1m(输入完毕请按回车)：\033[0m')
            Skycn_soft(search_name).download()
            print('\033[32;1m\n正在上传每个软件的详细信息至数据库...\033[0m')
            SoftDetailedInfo(search_name).get_soft_info()
            ending = '''
            \033[35;1m
-----------------上传至数据库结束-----------------\n\033[32;1m 
              所有信息上传数据库成功！\n
                    谢谢使用！\n
\033[35;1m-----------------上传至数据库结束-----------------\n
\033[0m
            '''
            print(ending)























