import requests
import json
from bs4 import BeautifulSoup
import pdfminer

if __name__ == "__main__":
     headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }
     url = 'https://www.guoxinlanqiao.com/api/news/find'
     data = {
        'status': '1',
        'project': 'dasai',
        'progid': '20',
        'pageno': '1',
        'pagesize': '1'
     }

     id_list = []#储存比赛信息id
     text_list = []#存比赛信息文件
    #  text_detail #储存比赛信息文件内容
     json_ids = requests.get(url=url,headers=headers,params=data).json()
     for dic in json_ids['datalist']:
         id_list.append(dic['nnid'])

     url_detail = 'https://www.guoxinlanqiao.com/api/web/news/selectone'#打开具体网页的界面并以jason的形式储存其中内容
     for ids in id_list:
        data_detail = {
            'nnid': ids
        }
        detail_json = requests.get(url=url_detail,headers=headers,params=data_detail).json()#detail_jason是具体的信息
        # print(detail_json)
        # print('----------------------------------------------------------------------')
        news_list = list(detail_json['news'].items())#将jason文件中dic类型转化为list
        for i in news_list[4]:  #将list中第五项content取出
            text_list.append(i)  
        
        text_detail = "".join(text_list[1])  #第五项元组的第二项取出（去除content：）并转化为Str类型存在text_detail中
        # print(text_detail)

        # pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # text_result = pattern.findall(text_detail)
        # print(text_result)

     with open('关于开展第十五届蓝桥杯大赛“全国高校备赛季”活动的通知.pdf', 'w',encoding='utf-8') as f:
         f.write(text_detail)
     with open('关于开展第十五届蓝桥杯大赛“全国高校备赛季”活动的通知.pdf', 'rb') as file:
         soup = BeautifulSoup(file, 'html.parser')
     text = soup.get_text()
     with open('output.txt', 'w',encoding = 'utf-8') as f:
         f.write(text)


            
        
        
    
           

         

    



        
