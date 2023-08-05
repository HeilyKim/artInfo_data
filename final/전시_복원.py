from bs4 import BeautifulSoup
import requests
import pandas as pd
from preProcessing import cleaned,getDates

title = []
contents = []
artist = []
date = []
imgs = []




def doGet(ahref):
    if ahref in ['/archives/20230612e','/archives/20210915i','/archives/20190909i','/archives/20201224d']:
        return
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
        date.append(aDate.text)

        aTitle = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > h1')
        title.append(aTitle.text)

        pTags = soup.select_one(
            'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div.mt-9.document > div > p:nth-child(6)')
        for span in pTags.find_all('span', class_='line'):
            partist.append(span.get_text())
        merged_artist = '\n'.join(partist)
        artist.append(merged_artist)

        for p in soup.find_all('p'):
            if 'class' not in p.attrs:
                pcontent.append(p.get_text())
        merged_text = '\n'.join(pcontent)
        contents.append(merged_text)

        for i in soup.find_all('img'):
            src = i.get('src')
            if "advertisements" in src or src.endswith(".gif"):
                continue
            pimg.append(f'https://neolook.com{src}')
        merged_img = '\n'.join(pimg)
        imgs.append(merged_img)

    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred while crawling {ahref}: {req_err}")
    except Exception as e:
        print(f"Error while crawling {ahref}: {e}")


text = requests.get("https://neolook.com/archives")
text.encoding = 'ms949'

soup = BeautifulSoup(text.text, 'html.parser')

# Replace "div_xpath" with the provided XPath for the div tag
div_element = soup.select_one(
    'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(11)')

if div_element:
    ul_tag = div_element.select_one(
        'body > div.flex > div.z-\[60\].flex-1.md\:ml-40.min-w-0 > div > div.px-1.md\:px-0 > div:nth-child(11) > ul')

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
# print('title:', len(title))
# print('artist:', len(artist))
# print('date:', len(date))
# print('contents:', len(contents))
# print('imgs:', len(imgs))
# print(date)
# print(artist)
myInfo = {'title': title, 'artist': artist, 'date': date, 'content': contents, 'img': imgs}
# # # for key, values in myInfo.items():
# # #     print(f"{key}: {values[:3]}")
myDF = pd.DataFrame(myInfo)
myDF['content'] = myDF['content'].apply(lambda x: x[0].strip() if isinstance(x, list) else x)
myDF['content'] = myDF['content'].apply(lambda x: x.strip()).apply(cleaned)
myDF[['start_date', 'end_date']] = myDF['date'].apply(getDates).apply(pd.Series)
myDF.drop(columns=['date'], inplace=True)
print(myDF.head(2))
