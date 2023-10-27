import requests
from bs4 import BeautifulSoup
import redis
import re 
import pymysql
import time

conn = redis.Redis()    #比较是否爬取的东西
class class_cet():
    def __init__(self):
        self.sample_cet = "报名"   #输入识别相关内容
        self.url = 'https://cet.neea.edu.cn/html1/category/16093/1124-1.htm'
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

        
    def crawl(self,url):
        res = requests.get(url, headers = self.header)
        if res.status_code == 200:
            res.encoding = 'utf=8'
            return res

    
    def spider(self):
        print('(CET)开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text,'lxml')
        list = soup.find('span', id='ReportIDname')
        # print(list.text)
        if re.search(self.sample_cet,list.text):
            title = list.text
            flg = conn.sadd('5zdaa',title) # 随机字符串，勿与之前相同
            if flg:
                #未爬取
                print(title+" is loading...")
                detail_url = 'https://cet.neea.edu.cn/'+list.a['href']
                #第二次请求网页
                detail_txt= self.crawl(detail_url).text
                detail_soup = BeautifulSoup(detail_txt,'lxml') #将网页信息加载到bs对象中
                
                details = detail_soup.find('span', id='ReportIDtext')
                try:
                    content = details.text #爬取对应标签里的text内容
                    self.save(content=content,title=title)
                    
                except KeyError:
                    print("KeyError occurs...")
            else:
                #已爬取，等待24h再次爬取
                print('(CET)暂无新信息,将于24小时后再次爬取...')
                
                
        print('*******************(CET)爬取完毕******************')
        time.sleep(10)
        # print('*************************************************************************************')
            
    
    def save(self,content,title):
        fp = open(title+'.txt','w',encoding='utf-8')
        fp.write('                                                                '+title+"\n"+content+"\n") #写入文件
        # self.todatabase(content=content,title=title)
        print(title+" has been loaded...")
    
    def run(self):
        print('*********************************(CET)爬虫程序开始运行...***********************************')
        self.spider()
            
    def todatabase(self,title,content):
        conn = pymysql.connect(host='127.0.0.1',port=3306,user='tester',password='Srdp20232',db = 'comp_srdp')
        cursor = conn.cursor()
        sql = "INSERT INTO comp (title, content) VALUES (%s, %s)"
        data = (title,content)
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()
        conn.close()
    
if __name__ == '__main__':
    x = class_cet()
    x.run()
    
    
    

    
    
