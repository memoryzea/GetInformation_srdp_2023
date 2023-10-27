import requests
from bs4 import BeautifulSoup
import redis
import pymysql


conn = redis.Redis()
class lanqiaobei():
    def __init__(self):
        self.headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }
        self.url = 'https://www.guoxinlanqiao.com/api/news/find'
        self.data = {
        'status': '1',
        'project': 'dasai',
        'progid': '20',
        'pageno': '1',
        'pagesize': '1'
     }
        
    
    def crawl(self,url,param):
        json_ids = requests.get(url=url,headers=self.headers,params=param).json()
        for dic in json_ids['datalist']:
            ids = dic['nnid']
            id_title = dic['title']
            
            
        url_detail = 'https://www.guoxinlanqiao.com/api/web/news/selectone'#打开具体网页的界面并以jason的形式储存其中内容
        data_detail = {
                'nnid': ids
        }
        detail_json = requests.get(url=url_detail,headers=self.headers,params=data_detail).json()
        return detail_json, id_title
    
    def spider(self):
        text_list = []#存比赛信息文件
        res, title = self.crawl(self.url,self.data)
        flg = conn.sadd('1sa0',title)
        if flg:
            news_list = list(res['news'].items())#将jason文件中dic类型转化为list
            for i in news_list[4]:  #将list中第五项content取出
                text_list.append(i)
            text_detail = "".join(text_list[1])
            self.save(content=text_detail,title=title)
            print('加载完成')
        else:
            import time
            print('暂无新信息,将于24小时后再次爬取...')
            time.sleep(60*60*24)
            self.spider()
            
        
    
    def run(self):
        while True:
            print('爬虫程序开始运行...')
            self.spider()
    
    
    def save(self,content,title):
        print('加载中')
        with open(title+'.pdf', 'w',encoding='utf-8') as f:
            f.write(content)
        with open(title+'.pdf', 'rb') as file:
            soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
        fp = open(title+'.txt','w',encoding='utf-8')
        fp.write(text)
        self.todatabase(content=text,title=title)
        
    def todatabase(self,title,content):
        conn = pymysql.connect(host='127.0.0.1',port=3306,user='tester',password='Srdp20232',db = 'comp_srdp')
        cursor = conn.cursor()
        sql = "INSERT INTO comp (title, content) VALUES (%s, %s)"
        data = (title,content)
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    x=lanqiaobei()
    x.run()


        
    
           

         

    



        
