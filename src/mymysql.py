#__auth__:"Sky lu"
# -*- coding:utf-8 -*-
import pymysql
from conf import settings


class DoMysql(object):
    def __init__(self):
        #创建连接
        self.conn = pymysql.Connect(
          host = settings.DATABASE_mysql['host'],
          port = settings.DATABASE_mysql['port'],
          user = settings.DATABASE_mysql['user'],
          password = settings.DATABASE_mysql['pwd'],
          db = settings.DATABASE_mysql['db'],
          charset = 'utf8',
          cursorclass = pymysql.cursors.DictCursor  #以字典的形式返回数据
        )
        #获取游标
        self.cursor = self.conn.cursor()

    #返回多条数据
    def fetchAll(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #插入一条数据
    def insert_one(self,sql):
        result = self.cursor.execute(sql)
        #self.conn.commit()
        return result

    #插入多条数据
    def insert_many(self,sql,datas):
        result = self.cursor.executemany(sql,datas)
        #self.conn.commit()
        return result

    #更新数据
    def update(self,sql):
        result = self.cursor.execute(sql)
        #self.conn.commit()
        return result

    #关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()