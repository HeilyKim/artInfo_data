import requests
from bs4 import BeautifulSoup

def doReq(ahref):
    text = requests.get(f"https://neolook.com/zb/{ahref}")
    text.encoding = 'ms949'
    soup = BeautifulSoup(text.text, "html.parser")
    title = soup.select_one('td.view-subject')
    print(title)
    content = soup.select_one('td.view-content')
    print(content.text)

text = requests.get("https://neolook.com/zb/zboard.php?id=post2005")
text.encoding='ms949'

soup = BeautifulSoup(text.text,"html.parser")
trs = soup.find_all('tr')

try:
    for tr in trs[2:]:
        a = tr.select_one('a')
        doReq(a['href'])

except:
    pass