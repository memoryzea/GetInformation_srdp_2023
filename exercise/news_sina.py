import requests
from bs4 import BeautifulSoup

newsHtml = requests.get("http://news.sina.com.cn/world/")
newsHtml.encoding = "utf-8"
# print(newsHtml.text)

soup = BeautifulSoup(newsHtml.text,"html.parser")
print(newsHtml.text)
# for newsItem in soup.select(".news-item"):
#     if len(newsItem.select("h2")) > 0:
#         title = newsItem.select("h2")[0].text
#         time = newsItem.select('.time')[0].text
#         href = newsItem.select('a')[0]['href']
#         url = title + time + href
#         with open('date.csv','a+') as file:
#             file.write(url)
#             print(url)
