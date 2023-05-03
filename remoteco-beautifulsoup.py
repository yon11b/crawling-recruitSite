# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Chrome(
#     'D:\seeds\SWEVER\CRAWLING-label-test\chromedriver_win32\chromedriver.exe')
# driver.get('https://remote.co/job/accounts-payable-coordinator-reconciliation-26/')
# print('time start')
# time.sleep(10)
# print('time finish')

# xbox = driver.find_element( By.CSS_SELECTOR,'# om-oqulaezshgjig4mgnmcn-optin > div > button')
# xbox.click()
# print('button clicked')
# time.sleep(10)
# print('button clicked and time finish')

# # card = driver.find_element(
# #     By.CSS_SELECTOR, '#job-109466')
# # print(card.text)
# # card.click()
# print('===========================TITLE============================')
# title = driver.find_element(
#     By.CSS_SELECTOR, 'body > main > div > div > div.col > div:nth-child(3) > div > h1')
# print(title.text)


# print('===========================COMPANY_NAME============================')
# company_name = driver.find_element(
#     By.CSS_SELECTOR, 'body > main > div > div > div.col > div:nth-child(3) > div > div.single_job_listing > div.company_sm > div > div.co_name > strong')
# print(company_name.text)

# print('===========================DESCRIPTION============================')
# desc = driver.find_element(
#     By.CSS_SELECTOR, '#jobsboard > tbody > tr.expand.expand-109466.active > td > div > div.description > div.markdown')
# print(desc.text)

# time.sleep(3)
# driver.close()
import requests
from bs4 import BeautifulSoup as bs
from lxml.html import fromstring
from openpyxl import Workbook
from itertools import cycle
import time
from random import choice
from fake_useragent import UserAgent
from requests.exceptions import ProxyError, SSLError, ConnectTimeout
import pymysql

# >>> DB 연결
con = pymysql.connect(host='127.0.0.1',user='root',password='ddun123!!',db='swever',charset='utf8')
cur = con.cursor()
# id=1
# title='test'
# company_name = 'test_company'
# description = 'test_description'

# >>> 크롤링
def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:50]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])  # /text빼고도 되는지 확인
            proxies.add(proxy)
    return proxies

headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    'User-Agent': str(UserAgent().chrome)
}
print(headers)

URL = 'https://remote.co/job/data-platform-engineer-model-life-cycle-2/'

proxy_server_list = []
proxy_server_list = list(get_proxies())
print(proxy_server_list)
while True:
    time.sleep(3)
    proxy = choice(proxy_server_list)
    print(proxy)
    proxies = {'http': proxy, 'https': proxy}
    try:
        resp = requests.get(URL, headers=headers,
                            proxies=proxies, verify=False, timeout=3)
        time.sleep(5)
        print('try..')
        print(resp.status_code)
        if (resp.status_code == "403"):
            print(resp)
        elif str(resp.status_code) == "200":
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
            parser = fromstring(resp.content)
            soup = bs(resp.text, "html.parser")
            print('===========================TITLE============================')
            title = soup.select_one(
                'body > main > div > div > div.col > div:nth-child(3) > div > h1')
            time.sleep(3)
            print(title.text)
            
            print('===========================COMPANY_NAME============================')            
            company_name = soup.select_one('div > div.single_job_listing > div.company_sm > div > div.co_name > strong')
            time.sleep(3)
            print(company_name.text)
            
            print('===========================DESCRIPTION============================')
            description = soup.select_one(
                'div:nth-child(3) > div > div.single_job_listing > div.job_description')
            time.sleep(3)
            print(description.text)
            break
    except (ProxyError, SSLError, ConnectTimeout) as e:
        print('except..')
        proxy_server_list.remove(proxy)
cur.execute("INSERT INTO job_recruit (title, company_name, description) values(%s,%s,%s)",
            [title.text, company_name.text, description.text])
con.commit()
con.close()
print("DONE...")
