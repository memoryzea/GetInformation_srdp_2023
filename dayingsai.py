import requests
from bs4 import BeautifulSoup
import redis


conn = redis.Redis()
class daying():
    def __init__(self):
        self.headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }
        self.url = 'https://www.chinaneccs.cn/api/v1/article/lists/neccsnews'
        self.data = {
            'limit': '1',
            'page': '1'
     }
        
    
    def crawl(self,url,param):
        json_ids = requests.post(url=url,headers=self.headers,data=param).json()
        for dic in json_ids['data']['list']:
            ids = dic['id']
            id_title = dic['title']
            
        
        url_detail = 'https://www.chinaneccs.cn/api/v1/article/detail/'+ids #打开具体网页的界面并以jason的形式储存其中内容
        data_detail = {
                'is_h5': '1'
        }
        detail_json = requests.post(url=url_detail,headers=self.headers,data=data_detail).json()
        return detail_json, id_title
    
    def spider(self):
        text_list = []#存比赛信息文件
        res, title = self.crawl(self.url,self.data)
        flg = conn.sadd('1sa0dsd',title) # 随机字符串，勿与之前相同
        if flg:
            news_list = list(res['data'].items())#将jason文件中dic类型转化为list
            for i in news_list[1]:  #将list中第2项content取出
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
        print('爬虫程序开始运行...')
        while True:
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
        
if __name__ == "__main__":
    x=daying()
    x.run()