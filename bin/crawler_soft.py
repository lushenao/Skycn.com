#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)


from core import main


if __name__ == '__main__':
    start = main.Start()
    start.run()