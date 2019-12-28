#__auth__:"Sky lu"
# -*- coding:utf-8 -*-
import os,json,requests,re
from conf import settings
from src.mymysql import DoMysql
from src.dict_to_mysql_update_value import dicttomysqlupdate
from src.progress_bar import ProgressBar

class SoftDetailedInfo(object):
    def __init__(self,search_name):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.search_name = search_name
        self.soft_desc = settings.soft_desc


    def get_soft_info(self):
        mysql = DoMysql()
        f = open(self.BASE_DIR + '/db/' + self.search_name + '.json', 'r')
        count = 0
        f_list = f.readlines()
        total = len(f_list)
        #print(total)
        for i in f_list:
            soft_data = json.loads(i)
            url = soft_data['软件页面链接']
            soft_name = soft_data['软件名称']
            r_text = requests.get(url).content.decode('utf-8','ignore').replace(' ','').replace('\r','').replace('\n','')
            soft_size = re.findall(r'<spanclass="t_title">大小：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_size`'] = "'"+ " ".join(str(i) for i in soft_size) + "'"
            soft_version = re.findall(r'<spanclass="t_title">版本：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_version`'] = "'"+" ".join(str(i) for i in soft_version)+ "'"
            soft_update_time = re.findall(r'<spanclass="t_title">更新：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_update_time`'] ="'"+ " ".join(str(i) for i in soft_update_time)+ "'"
            soft_operating_system_bit = re.findall(r'<spanclass="t_title">系统位数：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_operating_system_bit`'] = "'"+" ".join(str(i) for i in soft_operating_system_bit)+ "'"
            soft_comment = re.findall(r'<spanclass="t_title">评论：</span><spanclass="blue">(.*?)</span>条</div>', r_text)
            self.soft_desc['`soft_comment`'] = "'"+" ".join(str(i) for i in soft_comment)+ "'"
            soft_language = re.findall(r'<spanclass="t_title">语言：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_language`'] = "'"+" ".join(str(i) for i in soft_language)+ "'"
            soft_auth = re.findall(r'<spanclass="t_title">授权：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_auth`'] = "'"+" ".join(str(i) for i in soft_auth)+ "'"
            soft_operating_system = re.findall(r'<spanclass="t_title">适合系统：</span>(.*?)</div>', r_text)
            self.soft_desc['`soft_operating_system`'] = "'"+" ".join(str(i) for i in soft_operating_system)+ "'"
            #将数据插入数据库
            table = '`soft_info`'
            value = dicttomysqlupdate(self.soft_desc,len(self.soft_desc.keys()))
            #print(value)
            #sql = 'INSERT INTO {table}({keys}) VALUES ({values}） WHERE `soft_name = {soft_name}`)'.format(table=table, keys=keys, values=values, soft_name=soft_name)
            sql = "UPDATE %s SET %s where `soft_name` = '%s'" % (table,value,soft_name)
            #print(sql)
            try:
               mysql.insert_one(sql)
               #print('Successful')

            except Exception as e:
               print('Failed',e)
               mysql.conn.rollback()
            finally:
                count += 1
                ProgressBar(count,total).run()
        f.close()
        mysql.conn.commit()
        mysql.close()



#SoftDetailedInfo('qq').get_soft_info()




