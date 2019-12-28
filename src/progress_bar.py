#__auth__:"Sky lu"
# -*- coding:utf-8 -*-
import math,sys

class ProgressBar:
    def __init__(self, portion, total):
        '''
        进度条功能
        :param portion: 已经传输的数据量
        :param total: 总共的数据量
        :return:
        '''
        self.portion = portion
        self.total = total
    def run(self):
        part = self.total / 50
        count = math.ceil(self.portion / part)
        sys.stdout.write('\033[32;1m\r[%-50s] %.2f%%\033[0m' % (('#' * count), self.portion / self.total * 100))
        sys.stdout.flush()

        if self.portion >= self.total:
            sys.stdout.write('\n')
            return True