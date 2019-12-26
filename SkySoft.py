#__auth__:"Sky lu"
# -*- coding:utf-8 -*-
import gevent
from gevent import monkey
monkey.patch_all()

import requests,re
import os,sys,json,time



class Skysoft(object):



    def __init__(self,search_name):
        self.search_name = search_name
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.count = 0

    def req_text(self): #利用post获取搜索结果的html文本
        url = ('http://www.skycn.com/s.php')
        d = {'key': str(self.search_name)}
        r = requests.post(url, data=d)
        r_text = r.text.replace(' ', '')
        # 按行读取文本，然后去除换行符
        f = open(self.search_name + '.txt', 'w')
        f.write(r_text)
        f.close()
        r_new_text = ''
        f = open(self.search_name + '.txt', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            r_new_text += line
        f.close()
        os.remove(self.search_name + '.txt')
        return r_new_text

    def req_text_get(self,page): #利用get获取搜索结果第二页以后的html文本
        url = (r'http://www.skycn.com/index.php?ct=search&ac=softsea&key=%s&page=%s' % (self.search_name,page))
        r = requests.get(url)
        r_text = r.text.replace(' ', '')
        # 按行读取文本，然后去除换行符
        f = open(self.search_name + '.txt', 'w')
        f.write(r_text)
        f.close()
        r_get_text = ''
        f = open(self.search_name + '.txt', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            r_get_text += line
        f.close()
        os.remove(self.search_name + '.txt')
        return r_get_text

    def page_total(self):
        try:
            req_text = self.req_text()
            page_text = re.search(r'page-num(.*?)</div></div>', req_text).group()
            page_num = re.findall(r'\d+', page_text)
            page_num_total = max(list(map(int, page_num)))
            return page_num_total
        except:
            return 1

    def soft_info(self,soft_list): #获取当前页面的搜索软件信息
        for i in soft_list:
            soft_dict = {
                '软件名称': 0,
                '软件页面链接': 0,
                '下载链接': 0,
                '软件描述': 0,
                '图标下载链接': 0
            }
            try:
                soft_dl_links = re.findall(r'</p><ahref="(.*?)"class=', i)[0]
                soft_dl_links = " ".join(str(i) for i in soft_dl_links).replace(' ', '')
                soft_links = 'http://soft.hao123.com'+ re.search(r'/(.*?).html',i).group()
                soft_name = re.findall(r'title="">(.*?)</a>', i)[0]
                soft_name = " ".join(str(i) for i in soft_name).replace(' ','')
                soft_des = re.findall(r'<pclass="s-desc">(.*?)</p>', i)
                soft_des = " ".join(str(i) for i in soft_des)
                soft_icon = re.findall(r'imgsrc="(.*?)"alt="', i)
                #print(soft_icon)
                soft_icon = " ".join(str(i) for i in soft_icon).replace(' ', '')
            except Exception as e:
                #print(e)
                continue
            f = open(self.BASE_DIR + '/' + self.search_name + '.json', 'a')
            soft_dict['软件名称'] = str(soft_name)
            soft_dict['软件页面链接'] = str(soft_links)
            soft_dict['下载链接'] = str(soft_dl_links)
            soft_dict['软件描述'] = str(soft_des)
            soft_dict['图标下载链接'] = str(soft_icon)
            f.writelines(json.dumps(soft_dict, ensure_ascii=False) + '\n')
            f.close()
            self.count += 1
            #print('\033[32;1m%s软件信息爬取完成...\033[0m' % (soft_name))

    def soft_next_info(self,page):
        r_get_text = self.req_text_get(page)
        # print(r_get_text)
        soft_list = str(r_get_text).split('<divclass="list-con">')
        self.soft_info(soft_list)


    def download(self):
        soft_count = 0
        req_text = self.req_text()
        #print(req_text)
        page_total = self.page_total()
        enter = input('\033[32;1m一共搜索到%s页结果，请按任意键继续！\n\033[37;1m(取消搜索请输入Q)：\033[0m\033[0m' % page_total).strip()
        if enter == 'Q':
            start()
        start_time = time.time()
        soft_list = str(req_text).split('<divclass="list-con">') #根据软件分割文本
        if os.path.isfile(self.BASE_DIR + '/' + self.search_name + '.json'):  #当前目录已存在同名json文件，即删除
            os.remove(self.BASE_DIR + '/' + self.search_name + '.json')
        if int(page_total) == 1: #当搜索结果页面只有一页时
            self.soft_info(soft_list)
        else:
            self.soft_info(soft_list) #获取第一页搜索结果
            threads = [gevent.spawn(self.soft_next_info, page) for page in range(2, int(page_total) + 1)] #将每一页开启一个协程去下载
            #self.soft_info(soft_list)
            gevent.joinall(threads)#协程下载每个页面的搜索结果
        end_time = time.time()
        spend_time = end_time-start_time
        ending = '''
\033[34;1m
-----------------爬取结束-----------------
\033[32;1m在Skycn.com网站,搜索关键字[%s]一共爬取了[%s]个软件！

总共花费的时间是%s s

\033[32;1m文件保存在:\n\033[36;1m%s\n\033[34;1m
-----------------爬取结束-----------------\033[0m
        ''' % (self.search_name,self.count,round(spend_time,2),self.BASE_DIR)
        print(ending)



def start():
    while True:
        title = '''\033[34;1m
---Skycn.com网站爬取工具---\033[0m
        '''
        print(title)
        search_name = input('\033[32;1m您想要搜索的软件关键字是？\n\033[37;1m(输入完毕请按回车,退出程序请输入Q)：\033[0m').strip()
        if len(search_name) == 0:
            print('\033[31;1m请输入关键字!')
            continue
        if search_name == 'Q':
            break
        #pages = input('\033[32;1m您想要爬取总页数？\n\033[37;1m(输入完毕请按回车)：\033[0m')
        Skysoft(search_name).download()

if __name__ == '__main__':
    start()



