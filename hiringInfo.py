import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

brow = webdriver.Chrome()
title = []
content = []

def neoCrawling(key):
    brow.get("http://neolook.com/frame")
    iframe_element = brow.find_element(By.TAG_NAME, "iframe")
    brow.switch_to.frame(iframe_element)
    element = brow.find_element(By.CSS_SELECTOR,
                                "body > div.wrapper > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > form > input.input")
    element.send_keys(key)
    element.send_keys(Keys.ENTER)

try:
    for i in range(2, 4):
        neoCrawling("채용")
        time.sleep(2)
        brow.find_element(By.CSS_SELECTOR,
                          f"body > div.wrapper > table.table-width > tbody > tr:nth-child({i}) > td.column.subject > a").click()
        hiringTitle = brow.find_element(By.CLASS_NAME, "view-subject")
        hiringContent = brow.find_element(By.CLASS_NAME, "view-content")
        title.append(hiringTitle.text)
        content.append(hiringContent.text)
        time.sleep(2)
    hiringData = {'Title': title, 'Content': content}
    hiringDF = pd.DataFrame(hiringData)
    print(hiringDF)
    # hiringDF.to_csv('채용.csv', index=False, encoding='utf-8-sig')
    # print(hiringData)
    # print(hiringDF.loc[1, 'Content'])
except Exception as e:
    print(e)
finally:
    time.sleep(5)
    brow.close()
    brow.quit()


