from bs4 import BeautifulSoup
import requests
import pandas as pd
from preProcessing import getDates,cleaned
title = []
contents = []
date = []
img = []
def doGet(ahref):
    error = []
    try:
        pimg = []
        response = requests.get(f"https://neolook.com{ahref}")
        soup = BeautifulSoup(response.text, "html.parser", from_encoding='cp949')

        aDate = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(3)')
        if aDate:
            aDate = aDate.text
        else:
            aDate = soup.select_one(
            "body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2:nth-child(2) > span:nth-child(5)")
            aDate = aDate.text
        aTitle = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        aTitle = aTitle.text
        for i in soup.find_all('img'):
            src = i.get('src')
            if "advertisements" in src or src.endswith(".gif"):
                continue
            pimg.append(f'https://neolook.com{src}')
        merged_img = '\n'.join(pimg)
        aContent = soup.select_one("body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document")
        aContent = aContent.text
        # for i in range(8,20):
        #     aRegion = soup.select_one(
        #         f"body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child({i}) > span:nth-child(3)")
        #     if aRegion:
        #         aRegion = aRegion.text
        #
        #     aLocation = soup.select_one(
        #         f"body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child({i}) > span:nth-child(1)")
        #     if aLocation:
        #         aLocation = aLocation.text
        #         print(aLocation)
    except requests.exceptions.RequestException:
        error.append('err0r1')
    except Exception:
        error.append('err0r2')
    finally:
        if error is not None and len(error) == 0:
            title.append(aTitle)
            contents.append(aContent)
            date.append(aDate)
            img.append(merged_img)
        else:
            error = None


text = requests.get("https://neolook.com/archives")
text.encoding = 'ms949'

soup = BeautifulSoup(text.text, 'html.parser')

div_element = soup.select_one(
    'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(9)')

if div_element:
    ul_tag = div_element.select_one(
        'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(9) > ul')

    if ul_tag:
        li_tags = ul_tag.find_all('li')
        count = 0
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                href_link = a_tag['href']
                if href_link=='/archives/20230608d':
                    continue
                doGet(href_link)
                count += 1
                if count >= 12:
                    break
            else:
                continue
    else:
        print("no ul tag")
else:
    print("no such div tag")
# print(len(title))
# print(len(date))
# print(len(contents))
# print(len(location))
# print(len(region))
# #
myInfo ={'title':title,'date':date,'content':contents,'img':img}
myDF = pd.DataFrame(myInfo)
# myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
# myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF[['start_date', 'end_date']] = myDF['date'].apply(getDates).apply(pd.Series)
myDF.drop(columns=['date'], inplace=True)
# myDF.to_csv('upso.csv',index=False, encoding='utf-8-sig')
# print(myDF.head(2))
