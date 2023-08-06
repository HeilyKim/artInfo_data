from bs4 import BeautifulSoup
import requests
import pandas as pd
from preProcessing import cleaned,getDates
title = []
contents = []
artist = []
date = []
location = []
region = []
img = []
def doGet(ahref):
    error = []
    try:
        pimg = []
        text = requests.get(f"https://neolook.com{ahref}")
        # text.encoding = 'ms949'
        soup = BeautifulSoup(text.text, "html.parser",from_encoding='cp949')
        aRegion = soup.select_one("body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(10) > span:nth-child(2)")
        if aRegion:
            aRegion = aRegion.text
        else:
            aRegion = soup.select_one("body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(11) > span:nth-child(3)")
            aRegion = aRegion.text
        aTitle = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        aTitle = aTitle.text
        # title.append(aTitle.text)
        aArtist = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(1)')
        aArtist = aArtist.text
        # artist.append(aArtist.text)
        aDate = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(3)')
        aDate = aDate.text
        # date.append(aDate.text)
        pcontent = []
        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_content = '\n'.join(pcontent)

        aLocation = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(10) > span:nth-child(1)')
        if aLocation:
            aLocation = aLocation.text
        else:
            aLocation = soup.select_one(
                'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(9) > span:nth-child(1)')
            aLocation = aLocation.text
        for i in soup.find_all('img'):
            src = i.get('src')
            if "advertisements" in src or src.endswith(".gif"):
                continue
            pimg.append(f'https://neolook.com{src}')
        merged_img = '\n'.join(pimg)
    except requests.exceptions.RequestException:
        error.append('err0r1')
    except Exception:
        error.append('err0r2')
    finally:
        if error is not None and len(error) == 0:
            title.append(aTitle)
            contents.append(merged_content)
            artist.append(aArtist)
            date.append(aDate)
            location.append(aLocation)
            region.append(aRegion)
            img.append(merged_img)
        else:
            error = None

text = requests.get("https://neolook.com/archives")
text.encoding='ms949'

soup = BeautifulSoup(text.text, 'html.parser')

# Replace "div_xpath" with the provided XPath for the div tag
div_element = soup.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(6)')

if div_element:
    # Find the <ul> tag inside the <div> element
    ul_tag = div_element.select_one('body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(6) > ul')

    if ul_tag:
        li_tags = ul_tag.find_all('li')
        count = 0
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                href_link = a_tag['href']
                doGet(href_link)
                count += 1
                if count >= 20:
                    break
            else:
                continue
    else:
        print("no ul tag")
else:
    print("no such div tag")
# print(len(title))
# print(len(artist))
# print(len(date))
# print(len(contents))
# print(len(location))
# print(len(region))
# # print(contents)
# print(len(img))
myInfo ={'title':title,'artist':artist,'date':date,'region':region,'location':location,'content':contents,'img':img}
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF[['start_date', 'end_date']] = myDF['date'].apply(getDates).apply(pd.Series)
myDF.drop(columns=['date'], inplace=True)
myDF.to_csv('upso.csv',index=False, encoding='utf-8-sig')
# print(myDF.head(2))
