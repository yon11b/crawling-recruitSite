#from bs4 import BeautifulSoup as bs
import time
import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By

# >>> DB 연결
con = pymysql.connect(host='127.0.0.1', user='root',
                      password='ddun123!!', db='swever', charset='utf8')
cur = con.cursor()


driver = webdriver.Chrome(
    'D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
URL = 'https://www.stepstone.de/jobs--IT-system-engineer-m-w-d-Bundesweit-TOI-TOI-DIXI-Group-GmbH--9134347-inline.html?rltr=1_1_25_seorl_m_0_0_0_0_0_0'
driver.get(URL)
time.sleep(3)

print('===========================TITLE============================')
title = driver.find_element(
    By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[1]/div/div[3]/div[1]/article/div/div[1]/div[2]/div[1]/span[2]')
print(title.text)

time.sleep(2)
print('===========================COMPANY_NAME============================')
company_name = driver.find_element(
    By.XPATH, '//*[@id="app-CompanyCard"]/article/div/div/strong')
print(company_name.text)

print('===========================DESCRIPTION============================')
time.sleep(2)
description = driver.find_element(
    By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[1]/div/div[5]/div[1]/div/div')
print(description.text)

cur.execute("INSERT INTO job_recruit (title, company_name, description) values(%s,%s,%s)",
            [title.text, company_name.text, description.text])
con.commit()
con.close()
print("DONE...")
