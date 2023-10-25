import requests
from bs4 import BeautifulSoup
import redis
import re 
import html2text

conn = redis.Redis()    #比较是否爬取的东西
sample = "关于召开 2023 年全国大学生电子设计竞赛总结暨颁奖大会的通知"   #输入识别相关内容
class nuedc():
    def __init__(self):
        self.url = 'https://www.nuedc-training.com.cn/index/news/index/id/1'
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
        for list in soup.select('.new-main .newsMain-liText>a'):
            try:
                if re.search(sample,list.text):
                    title = list.text
                    # print(title)
                    flg = conn.sadd('1e1asaaas',title) # 随机字符串，勿与之前相同
                    if flg:
                        print(title+" is loading...")
                        detail_url = list['href']
                        detail_txt = self.crawl(detail_url).text
                        detail_soup = BeautifulSoup(detail_txt,'lxml')
                        content_element = detail_soup.find('div', class_='newsMain-content')
                        content = self.html_to_text(str(content_element))
                        self.save(content, title)
                    else:
                        import time
                        print('暂无新信息,将于24小时后再次爬取...')
                        time.sleep(60*60*24)
                        self.spider()
                else: 
                    pass    
            except KeyError:
                print("KeyError occurs...")
        # print('爬取完毕...')
    
    def html_to_text(self, html_content):
        h = html2text.HTML2Text()
        h.ignore_links = True  # 设置为True以忽略链接
        h.ignore_images = True  # 设置为True以忽略图像

        # 将 HTML 转换为 Markdown 格式的文本
        markdown_text = h.handle(html_content)
    
        return markdown_text
    
    def save(self,content,title):
        fp = open(title+'.txt','w',encoding='utf-8')
        fp.write('                                                                '+title+"\n"+content+"\n") #写入文件
        print(title+" has been loaded...\n-------------------------------------------------------------------------------\n")
    
    def run(self):
        print('爬虫程序开始运行...')
        while True:
            self.spider()
    
if __name__ == '__main__':
    x = nuedc()
    x.run()