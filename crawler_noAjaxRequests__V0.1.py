import requests
from bs4 import BeautifulSoup
import redis
import re 

conn = redis.Redis()    #比较是否爬取的东西
sample = "报名"   #输入识别相关内容
class auto():
    def __init__(self):
        self.url = 'https://cet.neea.edu.cn/html1/category/16093/1124-1.htm'
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
        }

        
    def crawl(self,url):
        res = requests.get(url, headers = self.header)
        if res.status_code == 200:
            res.encoding = 'utf=8'
            return res
    
    def parse(self):
        pass
    
    def spider(self):
        print('开始爬取目标网页...')
        res = self.crawl(self.url)
        soup = BeautifulSoup(res.text,'lxml')
        for list in soup.select('.listdiv li'):
            try:
                #如果满足条件，则将该标签属性与网页域名相加
                if list.span.get('id') =='ReportIDname':   
                    list_span = list.span
                    if re.search(sample,list_span.a.text): #查看符合条件的标签文本中是否含有识别内容
                        title = list_span.a.text 
                        #比较是否已经爬取
                        flg = conn.sadd('3',title)
                        if flg:
                            #未爬取
                            print(title+" is loading...")
                            detail_url = 'https://cet.neea.edu.cn/'+list_span.a['href']
                            #第二次请求网页
                            detail = requests.get(url=detail_url,headers=self.header)
                            detail.encoding = 'utf-8'
                            detail_txt = detail.text
                            detail_soup = BeautifulSoup(detail_txt,'lxml') #将网页信息加载到bs对象中
                
                            #遍历网页信息中的span标签
                            for details in detail_soup.select('.Condiv li>span'):
                                try:
                                    #如果满足条件，则永久化储存标签里的text内容
                                    if details.get('id') == 'ReportIDtext':
                                        content = details.text #爬取对应标签里的text内容
                                        self.save(content=content,title=title)
                                        print(title+" has been loaded...\n-------------------------------------------------------------------------------\n")
                                except KeyError:
                                    print("KeyError occurs...")
                        else:
                            #已爬取，等待24h再次爬取
                            import time
                            print('暂无新信息,将于24小时后再次爬取...')
                            time.sleep(60*60*24)
                            self.spider()
                            
                # # 页数遍历，待解决。。。# # # #
                # elif list.get('id') == 'PageNum':
                #     for ids in list.select('li>a'):
                #         if ids.get('id') == 'CBNext':
                #             new_url = 'https://cet.neea.edu.cn'+ids['href']
                #             self.crawl()
                #             self.spider(new_url)
                            
            except KeyError:
                print("KeyError occurs...")
        print('爬取完毕...')
    
    
    
    def save(self,content,title):
        content = content
        fp = open(title+'.txt','w',encoding='utf-8')
        fp.write('                                                                '+title+"\n"+content+"\n") #写入文件
        print(title+" has been loaded...\n-------------------------------------------------------------------------------\n")
    
    def run(self):
        while True:
            print('爬虫程序开始运行...')
            self.spider()
    
if __name__ == '__main__':
    x = auto()
    x.run()
    
    
##################################################
################### 10/23 ########################
##################################################
