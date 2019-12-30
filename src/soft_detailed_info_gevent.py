#__auth__:"Sky lu"
# -*- coding:utf-8 -*-
import os,json,requests,re
from conf import settings
from src.mymysql import DoMysql
from src.dict_to_mysql_update_value import dicttomysqlupdate
from src.progress_bar import ProgressBar
from DBUtils.PooledDB import PooledDB
import pymysql
from queue import Queue
import threading,time
import gevent

class SoftDetailedInfo(object):
    def __init__(self,search_name):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.search_name = search_name
        self.soft_desc = settings.soft_desc

    def mysql_conn(self):
        '''
        定义mysql连接信息
        :return: 返回mysql连接池
        '''
        maxconn = 50
        pool = PooledDB(
            pymysql,
            maxconn,
            host='',
            user='',
            port=3306,
            passwd='',
            db='',
            use_unicode=True
        )
        return pool
    def get_soft_info(self):
        '''
        定义多线程任务
        :return:
        '''
        q = Queue(maxsize=45) #定义最大队列，必须小于mysql最大连接池数
        mysql = self.mysql_conn()
        f = open(self.BASE_DIR + '/db/' + self.search_name + '.json', 'r')
        count = 0
        f_list = f.readlines()
        total = len(f_list)

        while f_list:
            f_list_line = f_list.pop() #从列表中弹出数据
            # self.update_soft_info(i, mysql)

            #t = threading.Thread(target=self.update_soft_info,args=(f_list_line, mysql,)) #弹出的每条数据开启一个线程
            t = gevent.spawn(self.update_soft_info, f_list_line, mysql)
            q.put(t) #将线程加入队列
            if (q.full() == True) or (len(f_list)==0) : #当队列满了或者列表中无数据了
                thread_list = [] #建立线程池
                while q.empty() == False: #当队列不为空时
                    t = q.get() #从队列中拿出一个线程
                    q.task_done()
                    thread_list.append(t) #将线程加入线程池
                    #t.start() #开启线程
                    count += 1
                    ProgressBar(count, total).run()  # 进度条
                    #continue
                gevent.joinall(thread_list)

            #print('第%s个线程启动完毕...' % count)
        mysql.close()
        f.close()



    def update_soft_info(self,file_list_line,mysql):
        soft_data = json.loads(file_list_line)
        url = soft_data['软件页面链接']
        soft_name = soft_data['软件名称']
        r_text = requests.get(url).content.decode('utf-8', 'ignore').replace(' ', '').replace('\r', '').replace('\n',
                                                                                                                '')
        soft_size = re.findall(r'<spanclass="t_title">大小：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_size`'] = "'" + " ".join(str(i) for i in soft_size) + "'"
        soft_version = re.findall(r'<spanclass="t_title">版本：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_version`'] = "'" + " ".join(str(i) for i in soft_version) + "'"
        soft_update_time = re.findall(r'<spanclass="t_title">更新：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_update_time`'] = "'" + " ".join(str(i) for i in soft_update_time) + "'"
        soft_operating_system_bit = re.findall(r'<spanclass="t_title">系统位数：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_operating_system_bit`'] = "'" + " ".join(str(i) for i in soft_operating_system_bit) + "'"
        soft_comment = re.findall(r'<spanclass="t_title">评论：</span><spanclass="blue">(.*?)</span>条</div>', r_text)
        self.soft_desc['`soft_comment`'] = "'" + " ".join(str(i) for i in soft_comment) + "'"
        soft_language = re.findall(r'<spanclass="t_title">语言：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_language`'] = "'" + " ".join(str(i) for i in soft_language) + "'"
        soft_auth = re.findall(r'<spanclass="t_title">授权：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_auth`'] = "'" + " ".join(str(i) for i in soft_auth) + "'"
        soft_operating_system = re.findall(r'<spanclass="t_title">适合系统：</span>(.*?)</div>', r_text)
        self.soft_desc['`soft_operating_system`'] = "'" + " ".join(str(i) for i in soft_operating_system) + "'"
        # 将数据插入数据库
        table = '`soft_info`'
        value = dicttomysqlupdate(self.soft_desc, len(self.soft_desc.keys()))
        # print(value)
        # sql = 'INSERT INTO {table}({keys}) VALUES ({values}） WHERE `soft_name = {soft_name}`)'.format(table=table, keys=keys, values=values, soft_name=soft_name)
        sql = "UPDATE %s SET %s where `soft_name` = '%s'" % (table, value, soft_name)
        # print(sql)
        con = mysql.connection()
        cur = con.cursor()
        try:
            cur.execute(sql)
            con.commit()
            # print('Successful')

        except Exception as e:
            print('Failed', e)
            con.rollback()
        finally:
            cur.close()
            con.close()





start_time = time.time()
SoftDetailedInfo('qq').get_soft_info()
stop_time = time.time()
print(stop_time - start_time)





