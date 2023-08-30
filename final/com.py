from bs4 import BeautifulSoup
import requests
import pandas as pd


title = []
content = []
cate = []
def doGet(ahref):
    text = requests.get(f"https://neolook.com/zb/{ahref}")
    text.encoding = 'ms949'
    soup = BeautifulSoup(text.text, "html.parser")
    aTitle = soup.select_one('td.view-subject')
    title.append(aTitle.text)
    aContent = soup.select_one('td.view-content')
    content.append(aContent.text)
    cate.append(target_value)



text = requests.get("https://neolook.com/zb/zboard.php?id=post2005&page=1&select_arrange=headnum&desc=asc&category=&sn=off&ss=on&sc=on&keyword=&sn1=&divpage=60")
text.encoding='ms949'

soup = BeautifulSoup(text.text,"html.parser")
# TODO
target_value = '광고홍보'
matching_tr_elements = []

tr_elements = soup.find_all('tr')
try:
    for tr_element in tr_elements:
        td_element = tr_element.find('td', class_='column-cate', text=target_value)
        if td_element:
            matching_tr_elements.append(tr_element)

    for tr_element in matching_tr_elements:
        a_tag = tr_element.find('a')
        if a_tag:
            link = a_tag['href']
            doGet(link)
        else:
            print("No <a> tag found inside the <td> element.")
    myInfo = {'title':title,'content':content,'cate':cate}
    myDF = pd.DataFrame(myInfo)
except:
    pass
