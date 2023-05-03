from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(
    ' D:\seeds\SWEVER\CRAWLING-label-test\chromedriver_win32\chromedriver.exe')
driver.get('https://remoteok.com/remote-jobs/remote-freelance-writer-iapwe-109466')
time.sleep(5)

print('===========================TITLE============================')
time.sleep(3)
title = driver.find_element(
    By.CSS_SELECTOR, '#jobsboard > tbody > tr.expand.expand-109466.active > td > div > div.description > h1')
print(title.text)


print('===========================COMPANY_NAME============================')
company_name = driver.find_element(
    By.CSS_SELECTOR, '#jobsboard > tbody > tr.expand.expand-109466.active > td > div > div.description > div.company_profile.dark > a:nth-child(2) > h2')
print(company_name.text)


print('===========================DESCRIPTION============================')
desc = driver.find_element(
    By.CSS_SELECTOR, '#jobsboard > tbody > tr.expand.expand-109466.active > td > div > div.description > div.markdown')
print(desc.text)


time.sleep(3)
driver.close()
