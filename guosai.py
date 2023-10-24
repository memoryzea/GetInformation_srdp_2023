import requests
from bs4 import BeautifulSoup
import redis
import re 
import PyPDF2
import io

conn = redis.Redis()    #比较是否爬取的东西
sample = "2023高教社杯全国大学生数学建模竞赛报名"   #输入识别相关内容
class auto():
    def __init__(self):
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
        print('开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text,'lxml')
        for list in soup.select('.item>a'):
            try:
                if re.search(sample,list.text):
                    title = list.text
                    flg = conn.sadd('1661415',title) # 随机字符串，勿与之前相同
                    if flg:
                        print(title+" is loading...")
                        detail_url = 'http://www.mcm.edu.cn'+list['href']
                        detail_txt = self.crawl(detail_url).text
                        detail_soup = BeautifulSoup(detail_txt,'lxml')
                        new_list = detail_soup.select('#divRightMain #divNodeAttachmentsList>.item>a')[0]
                        pdf_url = 'http://www.mcm.edu.cn'+new_list['href']
                        pdf_res = self.crawl(pdf_url)
                        self.save(content=pdf_res.content,title=title)
                    else:
                        import time
                        print('暂无新信息,将于24小时后再次爬取...')
                        time.sleep(60*60*24)
                        self.spider()
                else: 
                    print('无对应内容...')    
            except KeyError:
                print("KeyError occurs...")
        print('爬取完毕...')
    
    
    
    def save(self,content,title):

        fp = open(title+'.pdf','wb')
        fp.write(content) #写入文件
        print(title+" has been loaded...\n-------------------------------------------------------------------------------\n")
    
    def run(self):
        while True:
            print('爬虫程序开始运行...')
            self.spider()
    
if __name__ == '__main__':
    x = auto()
    x.run()