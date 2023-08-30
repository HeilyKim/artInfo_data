from bs4 import BeautifulSoup
import requests
import pandas as pd
from final.preProcessing import getDateForContest, cleaned
title = []
contents = []
date = []
img = []

def doGet(ahref):
    error = []
    try:
        aImgLink=[]
        pcontent = []
        response = requests.get(f"https://neolook.com{ahref}")
        soup = BeautifulSoup(response.text, "html.parser", from_encoding='cp949')

        aDate = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(3)')
        aDate = aDate.text
        if '접수기간' not in aDate:
            raise ValueError("Date does not contain '접수기간'")
        aTitle = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        aTitle = aTitle.text
        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_text = '\n'.join(pcontent)
        aImg = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > dl > dt > img')
        src = aImg.get('src')
        aImgLink = f'https://neolook.com{src}'

    except requests.exceptions.RequestException:
        error.append('err0r1')
    except Exception:
        error.append('err0r2')
    finally:
        if error is not None and len(error) == 0:
            title.append(aTitle)
            contents.append(merged_text)
            date.append(aDate)
            img.append(aImgLink)
        else:
            error = None


text = requests.get("https://neolook.com/archives")
text.encoding = 'ms949'

soup = BeautifulSoup(text.text, 'html.parser')

div_element = soup.select_one(
    'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(4)')

if div_element:
    ul_tag = div_element.select_one(
        'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(4) > ul')
    if ul_tag:
        li_tags = ul_tag.find_all('li')
        count = 0
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                href_link = a_tag['href']
                doGet(href_link)
            else:
                continue
    else:
        print("no ul tag")
else:
    print("no such div tag")

myInfo = {'title':title,'date':date,'content':contents,'img':img}
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF = getDateForContest(myDF, 'date')


