import requests
from bs4 import BeautifulSoup
import redis
import re 
import os


conn = redis.Redis()    # 比较是否爬取的东西
sample = ""   # 输入识别相关内容

class ncsisc():
    def __init__(self):
        self.url = 'https://www.caairobot.com/topics/notifications'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

    def crawl(self, url):
        res = requests.get(url, headers=self.header)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            return res

    def spider(self):
        print('开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text, 'lxml')
        for link in soup.select('div[id="outermain"] ul[class="list"]>li'):
            try:
                if re.search(sample, link.text):                    
                    title = link.text
                    flg = conn.sadd('1s阿saadadadasdadadda61', title)
                    if flg:
                        print(title + " is loading...")
                        detail_url = link.a['href']
                        detail_res = self.crawl(detail_url)
                        detail_soup = BeautifulSoup(detail_res.text, 'lxml')
                        for detail in detail_soup.select('#outermain .entry-content'):
                            detail_link = detail.find_all('img')
                            src_attributes = [img['src'] for img in detail_link]
                        # 先执行前面的代码以获取 src_attributes 列表
                        self.save(src_attributes,title)
                           
                    else:
                        import time
                        print('暂无新信息，将于24小时后再次爬取...')
                        time.sleep(60 * 60 * 24)
                        self.spider()
                else:
                    pass
            except KeyError:
                print("KeyError occurs...")
        print('爬取结束')
    




    def download_image(self, url, save_path):
        res = self.crawl(url)

        with open(save_path, 'wb') as f:
            f.write(res.content)


    def save(self, content, title):
        for idx, src in enumerate(content):
            save_path = os.path.join("", f"{title}_{idx}.jpg")  # 设置保存路径和文件名
            self.download_image(src, save_path)
        print(title + " images have been downloaded...\n-------------------------------------------------------------------------------\n")
    
    def run(self):
        print('爬虫程序开始运行...')
        while True:
            self.spider()
            
    
if __name__ == '__main__':
    x = ncsisc()
    x.run()

