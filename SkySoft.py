#__auth__:"Sky lu"
# -*- coding:utf-8 -*-

#__auth__:"Sky lu"
# -*- coding:utf-8 -*-


import requests,re
import os,sys,json


class Skysoft(object):
    def __init__(self,search_name):
        self.search_name = search_name
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
            f = open(self.BASE_DIR + '/' + search_name + '.json', 'a')
            soft_dict['软件名称'] = str(soft_name)
            soft_dict['软件页面链接'] = str(soft_links)
            soft_dict['下载链接'] = str(soft_dl_links)
            soft_dict['软件描述'] = str(soft_des)
            soft_dict['图标下载链接'] = str(soft_icon)
            f.writelines(json.dumps(soft_dict, ensure_ascii=False) + '\n')
            f.close()
            print('\033[32;1m%s软件信息爬取完成...\033[0m' % (soft_name))





    def download(self):
        req_text = self.req_text()
        #print(req_text)
        page_total = self.page_total()
        soft_list = str(req_text).split('<divclass="list-con">') #根据软件分割文本
        if int(page_total) == 1: #当搜索结果页面只有一页时
            self.soft_info(soft_list)
            print('\033[32;1m所有软件爬取完成,文件保存在\n\033[36;1m%s\n\033[32;1m目录下\033[0m' % (self.BASE_DIR))
        if os.path.isfile(self.BASE_DIR + '/' + search_name + '.json'):
            os.remove(self.BASE_DIR + '/' + search_name + '.json')
        self.soft_info(soft_list)
        for page in range(2,int(page_total)+1):
            r_get_text = self.req_text_get(page)
            #print(r_get_text)
            soft_list = str(r_get_text).split('<divclass="list-con">')  # 以video的项目模型为分界分割html文本
            self.soft_info(soft_list)
            print('\033[32;1m所有软件爬取完成,文件保存在\n\033[36;1m%s\n\033[32;1m目录下\033[0m' % (self.BASE_DIR))



if __name__ == '__main__':
    while True:
        search_name = input('\033[32;1m您想要搜索的软件关键字是？\n\033[37;1m(输入完毕请按回车)：\033[0m')
        #pages = input('\033[32;1m您想要爬取总页数？\n\033[37;1m(输入完毕请按回车)：\033[0m')
        Skysoft(search_name).download()


