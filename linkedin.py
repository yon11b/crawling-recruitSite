from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html import fromstring
import re
import requests
import pymysql
import time
import emoji
from random import choice
from requests.exceptions import ProxyError, SSLError, ConnectTimeout


def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:20]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])  # /text빼고도 되는지 확인
            proxies.add(proxy)
    return proxies


# >>> DB 연결
con = pymysql.connect(host='127.0.0.1', user='root',
                      password='ddun123!!', db='swever', charset='utf8')
cur = con.cursor()

proxy_server_list = list(get_proxies())
while True:
    try:
        proxy = choice(proxy_server_list)
        print(proxy)
        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy": proxy,
        #     "ftpProxy": proxy,
        #     "sslProxy": proxy,
        #     "proxyType": "MANUAL"
        # }

        driver = webdriver.Chrome(
            'D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
        URL = 'https://www.linkedin.com/jobs/search?'

        INIT_URL = 'https://www.linkedin.com/jobs/search?keywords=It&location=%EC%8B%B1%EA%B0%80%ED%8F%AC%EB%A5%B4&geoId=102454443&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        driver.get(INIT_URL)
        driver.set_window_size(1500, 800)

        time.sleep(10)
        driver.implicitly_wait(time_to_wait=60)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
        break
    except (ProxyError, SSLError, ConnectTimeout) as e:
        print('except..')
        proxy_server_list.remove(proxy)
# 화면에 보이는 JOB LIST들 다 가져와서 jobs_list 배열에 저장.
jobs_list = driver.find_elements(
    By.CSS_SELECTOR, "div.base-card.relative.w-full.hover\:no-underline.focus\:no-underline.base-card--link.base-search-card.base-search-card--link.job-search-card")

# VARIRABLES
KEYWORD = 'it'
LOCATION = 'singapore'
OFFSET = '&trk=public_jobs_jobs-search-bar_search-submit'
PAGENUM = '0'
GEOID = '102454443'  # 나라 고유 번호?
time.sleep(5)
job_detail_urls = []
for i, job in enumerate(jobs_list):
    href = job.find_element(By.TAG_NAME, "a").get_attribute('href')
    start = href.find("-") + 1
    end = href.find("?")
    get_jobID = href[start:end].split("-")[-1]      # 처음 나오는 숫자를 추출
    job_detail_url = URL+'keywords='+KEYWORD+'&location='+LOCATION+'&geoId=102454443'+OFFSET+'&currentJobId='+str(get_jobID) + \
        '&position='+str(i+1)+'&pageNum='+PAGENUM
    print('<<<<<<<<<<<<<<<<<JOB_DETAIL_URL')
    print(job_detail_url)
    job_detail_urls.append(job_detail_url)

job_detail_infos = []
for detail_url in job_detail_urls:
    driver.get(url=detail_url)
    driver.implicitly_wait(time_to_wait=60)
    print('===========================PRINT-URL============================')
    print(detail_url)
    print('================================================================')
    job_detail_info = []
    time.sleep(2)
    print(1)
    title = driver.find_element(
        By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > a > h2")
    time.sleep(2)
    print(2)
    driver.implicitly_wait(time_to_wait=60)
    time.sleep(2)
    print(3)

    print('===========================TITLE============================')
    print(title.text)
    job_detail_info.append(title.text)

    company_name = driver.find_element(
        By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span:nth-child(1) > a")
    print('===========================COMPANY_NAME============================')
    print(company_name.text)
    job_detail_info.append(company_name.text)

    description = driver.find_element(
        By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > div > section.core-section-container.my-3.description > div")
    print('===========================DESCRIPTION============================')
    # print(description.text)
    job_detail_info.append(description.text)

    job_detail_infos.append(job_detail_info)
    print(job_detail_infos)

    cur.execute("INSERT INTO job_recruit (title, company_name, description) values(%s,%s,%s)",
                [title.text, company_name.text, description.text])
    con.commit()

con.close()
driver.close()
