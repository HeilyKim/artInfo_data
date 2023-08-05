import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlex
brow = webdriver.Chrome()
brow.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_type_radio')
brow.switch_to.frame('iframeResult') #id
ele = brow.find_element(By.ID,"html") #element -> 1개 elements -> 여러개
ele.click()
pele = brow.find_elements(By.TAG_NAME,"p")
for i in pele:
    print(i.text)
    sqlex.insert_data(i.text)
time.sleep(2)
brow.quit()