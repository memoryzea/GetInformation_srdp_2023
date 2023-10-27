import html2text
import requests
from bs4 import BeautifulSoup
import redis
import pymysql
# import re 

conn = redis.Redis()    #比较是否爬取的东西
# sample = "报名"   #输入识别相关内容
class class_mcm():
    def __init__(self):
        self.url = 'https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php'
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

        
    def crawl(self,url):
        res = requests.get(url, headers = self.header)
        if res.status_code == 200:
            res.encoding = 'utf=8'
            return res

    
    def spider(self):
        print('开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text,'lxml')
        title = soup.find('span', style='font-size:16.0pt;mso-bidi-font-size:12.0pt')
        # print(title.text)
        flg = conn.sadd('5爱是caaxzxaaa',title.text) # 随机字符串，勿与之前相同
        if flg:
            print('MCM is downloading...')
            content_element = soup.find('div', class_='Section1')
            content = self.html_to_text(str(content_element))
            self.save(content)
        else:
            #已爬取，等待24h再次爬取
            import time
            print('暂无新信息,将于24小时后再次爬取...')
            time.sleep(60*2)
            self.spider()
        print('爬取完毕')
        print('*************************************************************************************')
            
    
    def html_to_text(self, html_content):
        h = html2text.HTML2Text()
        h.ignore_links = True  # 设置为True以忽略链接
        h.ignore_images = True  # 设置为True以忽略图像
        # 将 HTML 转换为 Markdown 格式的文本
        markdown_text = h.handle(html_content)
        return markdown_text
    
    def save(self,content):
        fp = open('MCM通知.txt','w',encoding='utf-8')
        fp.write(content) #写入文件
        # self.todatabase(content=content,title='MCM通知')
        print("MCM通知.txt has been loaded...")
    
    def run(self):
        print('爬虫程序开始运行...')
        while True:
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
    x = class_mcm()
    x.run()
    
    
    
    
    
    
    
