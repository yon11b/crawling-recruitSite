from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql

# >>> DB 연결
con = pymysql.connect(host='127.0.0.1', user='root',
                      password='ddun123!!', db='swever', charset='utf8')
cur = con.cursor()

driver = webdriver.Chrome(
    'D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
URL = 'https://www.glassdoor.com/Job/san-francisco-ca-front-end-engineer-jobs-SRCH_IL.0,16_IC1147401_KO17,35.htm?src=GD_JOB_AD&srs=JOBS_HOME_RECENT_SEARCHES&jl=1005579680918&ao=1136043&s=58&guid=00000187e08d26caa000e1a1a285f308&pos=102&t=SR-JOBS-HR&vt=w&uido=6370B969392800D7D9E2B3D603450E72&cs=1_dedfd3ac&cb=1683099560090&jobListingId=1005579680918&jrtk=3-0-1gvg8q9ndi9jp801-1gvg8q9o3gfoj800-b1b6fe2d4b485731-'

driver.get(URL)
time.sleep(3)

print('===========================TITLE============================')
time.sleep(3)
title = driver.find_element(
    By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]')
title = title.text
print(title)


print('===========================COMPANY_NAME============================')
company_name = driver.find_element(
    By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div')
company_name = company_name.text
company_name = company_name[:company_name.index('\n')]
print(company_name)


print('===========================DESCRIPTION============================')
description = driver.find_element(
    By.XPATH, '//*[@id="JobDesc1005579680918"]/div')
description = description.text
print(description)


cur.execute("INSERT INTO job_recruit (title, company_name, description) values(%s,%s,%s)",
            [title, company_name, description])
con.commit()
con.close()
driver.close()
print("DONE...")
