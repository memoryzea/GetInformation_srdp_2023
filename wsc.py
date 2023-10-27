import requests
from bs4 import BeautifulSoup
import redis
import re 
import html2text
import pymysql
import time

conn = redis.Redis()    # 比较是否爬取的东西

class class_wsc():
    def __init__(self):
        self.wsc_sample = ""   # 输入识别相关内容
        self.url = 'http://worldskillschina.mohrss.gov.cn/sszx/tzwj/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

    def crawl(self, url):
        res = requests.get(url, headers=self.header)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res

    def spider(self):
        print('(WSC)开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text, 'lxml')
        link = soup.find('div',class_='list clearfix')
        tag =link.find('div',class_='listitem')
        try:
            if re.search(self.wsc_sample, tag.text):
                title = tag.a.text
                flg = conn.sadd('1达da61', title)
                if flg:
                    print(title + " is loading...")
                    detail_url = 'http://worldskillschina.mohrss.gov.cn' + tag.a['href']
                    detail_res = self.crawl(detail_url)
                    detail_soup = BeautifulSoup(detail_res.text, 'lxml')
                    content_element = detail_soup.find('div', class_='detail-content')
                    content = self.html_to_text(str(content_element))
                    self.save(content, title)
                else:
                    print('(WSC)暂无新信息，将于24小时后再次爬取...')

            else:
                pass
        except KeyError:
            print("KeyError occurs...")
        print('****************************(WSC)爬取结束***********************************')
        time.sleep(10)
    
    def html_to_text(self, html_content):
        h = html2text.HTML2Text()
        # h.ignore_links = True  # 设置为True以忽略链接
        h.ignore_images = True  # 设置为True以忽略图像

        # 将 HTML 转换为 Markdown 格式的文本
        markdown_text = h.handle(html_content)
    
        return markdown_text




    def save(self, content, title):
        fp = open(title + '.txt', 'w', encoding='utf-8')
        fp.write('# ' + title + "\n" + content + "\n")  
        # self.todatabase(content=content,title=title)
        print(title + " has been loaded...")
        
    
    
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
        print('**************************(WSC)爬虫程序开始运行...*****************************')
        self.spider()
            
    
if __name__ == '__main__':
    x = class_wsc()
    x.run()
