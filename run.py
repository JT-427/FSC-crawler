from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
safari = webdriver.Safari()
safari.get("https://www.fsc.gov.tw/ch/home.jsp?id=97&parentpath=0%2C2&mcustomize=")

bsobj = BeautifulSoup(safari.page_source, 'lxml')
t = bsobj.find('div', attrs={'class': 'newslist'})

data = pd.DataFrame(columns=['編號', '公告日期', '資料來源', '標題', '內文'])
for row in t.findAll('li')[1:]:
    attributes = row.findAll('span')
    no = attributes[0].text
    date = attributes[1].text
    unit = attributes[2].text
    urlback = attributes[3].find('a').get('href')
    url = 'https://www.fsc.gov.tw/ch/' + urlback

    safari.get(url)
    bsobj2 = BeautifulSoup(safari.page_source, 'lxml')
    title = bsobj2.find('div', attrs={'class':'subject'}).text.strip()
    content = bsobj2.find('div', attrs={'class':'page-edit'}).text


    newrow = {
        '編號':no,
        '公告日期':date,
        '資料來源':unit,
        '標題':title,
        '內文':content
    }
    data = data.append(newrow, ignore_index=True)

data.to_csv("金管會公告.csv")
