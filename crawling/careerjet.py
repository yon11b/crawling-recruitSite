from urllib.request import Request, urlopen, HTTPError
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import csv

base_url = "https://www.careerjet.co.uk/search/jobs?s=developer&l=United+Kingdom"

driver = webdriver.Chrome("chromedriver")
driver.get(url=base_url)
driver.implicitly_wait(time_to_wait=60)

jobs_list = driver.find_elements(By.CSS_SELECTOR, ".job.clicky")
job_detail_urls = []

for job in jobs_list:
    job_detail_url = job.find_element(By.TAG_NAME, "a").get_attribute('href')
    job_detail_urls.append(job_detail_url)
    # if len(job_detail_urls) == 5:
    #     break

# for job_detail_url in job_detail_urls:
#     print(job_detail_url)

# href="/jobad/gbe7ea5fc1187b8ad2a62c440e7a0725df"

# job_detail_info = [job_description_title, job_company_name, job_company_loaction, job_company_description, job_company_urls]
job_detail_infos = []

for detail_url in job_detail_urls:
    driver.get(url=detail_url)
    job_detail_info = []
    driver.implicitly_wait(time_to_wait=60)
    job_description_title = driver.find_element(By.CSS_SELECTOR, ".container").find_element(By.TAG_NAME, "h1").get_attribute("innerText")
    job_detail_info.append(job_description_title)
    job_company_name = driver.find_element(By.CSS_SELECTOR, ".company").get_attribute("innerText")
    job_detail_info.append(job_company_name)
    job_company_loaction = driver.find_element(By.CSS_SELECTOR, ".details").find_element(By.TAG_NAME, "span").get_attribute("innerText")
    job_detail_info.append(job_company_loaction)
    job_company_description = driver.find_element(By.CSS_SELECTOR, ".content").get_attribute("innerText")
    #job_detail_info.append(job_company_description)
    job_company_urls = driver.find_element(By.CSS_SELECTOR, ".source").find_element(By.TAG_NAME, "a").get_attribute('href')
    job_detail_info.append(job_company_urls)
    job_detail_infos.append(job_detail_info)
    print(job_detail_infos)
print(job_detail_infos)

# driver.get(url=job_detail_urls[1])
# driver.implicitly_wait(time_to_wait=60)
# print("Title")
# print(driver.find_element(By.CSS_SELECTOR, ".container").find_element(By.TAG_NAME, "h1").get_attribute("innerText"))
# print("Name")
# print(driver.find_element(By.CSS_SELECTOR, ".company").get_attribute("innerText"))
# print("Location")
# print(driver.find_element(By.CSS_SELECTOR, ".details").find_element(By.TAG_NAME, "span").get_attribute("innerText"))
# print("description")
# print(driver.find_element(By.CSS_SELECTOR, ".content").get_attribute("innerText"))
# print("url")
# print(driver.find_element(By.CSS_SELECTOR, ".source").find_element(By.TAG_NAME, "a").get_attribute('href'))


# cp949
# euc-kr
# utf-16
# utf-8
# ascii

# 현재 £인코딩이 안됨 

f = open(f'careerjet.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)
for job_detail_info in job_detail_infos:
    csvWriter.writerow(job_detail_info)

f.close()









