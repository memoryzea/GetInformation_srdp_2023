import requests
from bs4 import BeautifulSoup
if __name__ == "__main__":
     headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }
     url = 'https://cet.neea.edu.cn/html1/category/16093/1124-1.htm'
     res = requests.get(url=url,headers=headers)
     res.encoding = 'utf-8'
     res_txt = res.text
     soup = BeautifulSoup(res_txt,'lxml') #将网页信息加载到bs对象中
     
     #遍历网页信息中的span标签
     for list in soup.select('.listdiv li>span'):
        try:
            #如果满足条件，则将该标签属性与网页域名相加
            if list.get('id') =='ReportIDname':   
                print(list.a.text+" is loading...")
                title = list.a.text 
                detail_url = 'https://cet.neea.edu.cn/'+list.a['href']
                
                #第二次请求网页
                detail = requests.get(url=detail_url,headers=headers)
                detail.encoding = 'utf-8'
                detail_txt = detail.text
                detail_soup = BeautifulSoup(detail_txt,'lxml') #将网页信息加载到bs对象中
                
                #遍历网页信息中的span标签
                for details in detail_soup.select('.Condiv li>span'):
                    try:
                        #如果满足条件，则永久化储存标签里的text内容
                        if details.get('id') == 'ReportIDtext':
                            content = details.text #爬取对应标签里的text内容
                            fp = open(title+'.txt','w',encoding='utf-8')
                            fp.write('                                                                '+title+"\n"+content+"\n") #写入文件
                            print(title+" has been loaded...\n-------------------------------------------------------------------------------\n")
                    except KeyError:
                        print("KeyError occurs...")
        except KeyError:
            print("KeyError occurs...")
