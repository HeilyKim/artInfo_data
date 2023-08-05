from bs4 import BeautifulSoup
import requests
import pandas as pd
from preProcessing import cleaned,getDates
title = []
contents = []
artist = []
date = []

def doGet(ahref):
    try:
        text = requests.get(f"https://neolook.com{ahref}")
        # text.encoding = 'ms949'
        soup = BeautifulSoup(text.text, "html.parser",from_encoding='cp949')
        aTitle = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        title.append(aTitle.text)
        aArtist = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(1)')
        artist.append(aArtist.text)
        aDate = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(3)')
        date.append(aDate.text)
        pcontent = []
        content = []
        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_text = '\n'.join(pcontent)
        content.append(merged_text)
        contents.append(content)
    except:
        pass

text = requests.get("https://neolook.com/archives")
text.encoding='ms949'

soup = BeautifulSoup(text.text, 'html.parser')

# Replace "div_xpath" with the provided XPath for the div tag
div_element = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(6)')

if div_element:
    # Find the <ul> tag inside the <div> element
    ul_tag = div_element.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(6) > ul')

    if ul_tag:
        # Find the <li> tag inside the <ul> tag
        li_tags = ul_tag.find_all('li')
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                href_link = a_tag['href']
                # print(href_link)
                doGet(href_link)
            else:
                continue
    else:
        print("no ul tag")
else:
    print("no such div tag")
# print(title)
# print(len(artist))
# print(len(date))
# print(len(contents))
myInfo = {'title':title,'artist':artist,'date':date,'content':contents}
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)

myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF[['start_date', 'end_date']] = myDF['date'].apply(getDates).apply(pd.Series)
myDF.drop(columns=['date'], inplace=True)
print(myDF.head(2))
