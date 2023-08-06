from bs4 import BeautifulSoup
import requests
import pandas as pd
from preProcessing import getDates,cleaned
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
        pcontent = []
        pimg = []
        partist = []
        response = requests.get(f"https://neolook.com{ahref}")
        if response.status_code != 200:
            print(f"Error: {response.status_code} - Failed to get content from {ahref}")
            return

        soup = BeautifulSoup(response.text, "html.parser", from_encoding='cp949')

        aDate = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h2 > span:nth-child(3)')
        aDate = aDate.text
        aTitle = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        aTitle = aTitle.text

        pTags = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(6)')
        for span in pTags.find_all('span', class_='line'):
            partist.append(span.get_text())
        merged_artist = '\n'.join(partist)
        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_content = '\n'.join(pcontent)
        for i in soup.find_all('img'):
            src = i.get('src')
            if "advertisements" in src or src.endswith(".gif"):
                continue
            pimg.append(f'https://neolook.com{src}')
        merged_img = '\n'.join(pimg)
        for i in range(8,20):
            aRegion = soup.select_one(
                f"body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child({i}) > span:nth-child(3)")
            if aRegion:
                aRegion = aRegion.text
            aLocation = soup.select_one(
                f"body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child({i}) > span:nth-child(1)")
            if aLocation:
                aLocation = aLocation.text
    except requests.exceptions.RequestException:
        error.append('err0r1')
    except Exception:
        error.append('err0r2')
    finally:
        if error is not None and len(error) == 0:
            title.append(aTitle)
            contents.append(merged_content)
            artist.append(merged_artist)
            date.append(aDate)
            location.append(aLocation)
            region.append(aRegion)
            img.append(merged_img)
        else:
            error = None


text = requests.get("https://neolook.com/archives")
text.encoding = 'ms949'

soup = BeautifulSoup(text.text, 'html.parser')

# Replace "div_xpath" with the provided XPath for the div tag
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
                doGet(href_link)
                count += 1
                if count >= 14:
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
myInfo ={'title':title,'artist':artist,'date':date,'region':region,'location':location,'content':contents,'img':img}
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF[['start_date', 'end_date']] = myDF['date'].apply(getDates).apply(pd.Series)
myDF.drop(columns=['date'], inplace=True)
print(myDF.head(2))
