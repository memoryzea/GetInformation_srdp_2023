import requests
from bs4 import BeautifulSoup
import redis
import re 
import PyPDF2
import pymysql
import time


conn = redis.Redis()    #比较是否爬取的东西
class class_guosai():
    def __init__(self):
        self.sample_guosai = ""   #输入识别相关内容
        self.url = 'http://www.mcm.edu.cn/html_cn/block/20ead73cbcf5a1c24b91947f98d7aac2.html'
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }


    def crawl(self,url):
        res = requests.get(url, headers = self.header)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res

    
    def spider(self):
        print('(GUOSAI)开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text,'lxml')
        div = soup.find('div',id='divRightNodes')
        list = div.find('div',class_='item')
        try:
            if re.search(self.sample_guosai,list.a.text):
                title = list.a.text
                flg = conn.sadd('1asa15',title) # 随机字符串，勿与之前相同
                if flg:
                    print(title+" is loading...")
                    detail_url = 'http://www.mcm.edu.cn'+list.a['href']
                    detail_txt = self.crawl(detail_url).text
                    detail_soup = BeautifulSoup(detail_txt,'lxml')
                    new_div = detail_soup.find('div', id='divNodeAttachmentsList')
                    new_list = new_div.find('div', class_='item').a
                    pdf_url = 'http://www.mcm.edu.cn'+new_list['href']
                    pdf_res = self.crawl(pdf_url)
                    self.save(content=pdf_res.content,title=title)
                else:
                    print('(GUOSAI)暂无新信息,将于24小时后再次爬取...')
            else: 
                pass
        except KeyError:
            print("KeyError occurs...")
        print('*************************(GUOSAI)爬取完毕...********************')
        time.sleep(10)
        # print('*************************************************************************************')
    
    
    
    def save(self,content,title):

        fp = open(title+'.pdf','wb')
        fp.write(content) #写入文件
        pdf_file = open(title+'.pdf', 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        with open(title+'.txt', 'w',encoding='utf-8') as txt_file:
            txt_file.write(text)
        pdf_file.close()
        # self.todatabase(content=text,title=title)
        print(title+" has been loaded...")
    
    def todatabase(self,title,content):
        conn = pymysql.connect(host='127.0.0.1',port=3306,user='tester',password='Srdp20232',db = 'comp_srdp')
        cursor = conn.cursor()
        sql = "INSERT INTO comp (title, content) VALUES (%s, %s)"
        data = (title,content)
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()
        conn.close()
        
    def run(self):
        print('*****************************(GUOSAI)爬虫程序开始运行...********************************')
        self.spider()
    
if __name__ == '__main__':
    x = class_guosai()
    x.run()
