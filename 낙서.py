from bs4 import BeautifulSoup
import requests
import pandas as pd
from final.preProcessing import cleaned
title = []
contents = []


def doGet(ahref):
    error = []
    try:
        pimg = []
        pcontent = []
        response = requests.get(f"https://neolook.com{ahref}")
        soup = BeautifulSoup(response.text, "html.parser", from_encoding='cp949')
        aTitle = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        aTitle = aTitle.text
        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_text = '\n'.join(pcontent)
    except requests.exceptions.RequestException:
        error.append('err0r1')
    except Exception:
        error.append('err0r2')
    finally:
        if error is not None and len(error) == 0:
            title.append(aTitle)
            contents.append(merged_text)
        else:
            error = None


text = requests.get("https://neolook.com/archives")
text.encoding = 'ms949'

soup = BeautifulSoup(text.text, 'html.parser')

# Replace "div_xpath" with the provided XPath for the div tag
div_element = soup.select_one(
    'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(8)')

if div_element:
    ul_tag = div_element.select_one(
        'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(8) > ul')
    if ul_tag:
        li_tags = ul_tag.find_all('li')
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

# print(len(title))
# print(len(contents))
myInfo ={'title':title,'content':contents}
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
# myDF.to_csv('pred.csv',index=False, encoding='utf-8-sig')
# print(myDF.head(2))
