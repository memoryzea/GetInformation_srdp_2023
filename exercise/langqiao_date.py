import requests
import json
from bs4 import BeautifulSoup

newsHtml = requests.get("https://dasai.lanqiao.cn/notices/")
newsHtml.encoding = "utf-8"

soup = BeautifulSoup(newsHtml.text,"html.parser")
for newsItem in soup.select(".notice-card"):
    if len(newsItem.select("a.title")) > 0:
        title = newsItem.select("a.title")[0].text
        href = newsItem.select('a')[0]['href']
        url = title + href
        with open('date_1.cvs','w') as file:
            file.write(url)
            print(url)

# import requests
# from bs4 import BeautifulSoup

# url = 'https://dasai.lanqiao.cn/notices/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# for notice in soup.select('.notice-card'):
#     title = notice.select_one('.title').text.strip()
#     link = notice.select_one('a')['href']
#     print(f'{title} ({link})')
