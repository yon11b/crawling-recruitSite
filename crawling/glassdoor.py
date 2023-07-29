# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import requests

# driver = webdriver.Chrome(
#     'D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
# driver.get('https://www.glassdoor.com/Job/san-francisco-ca-front-end-engineer-jobs-SRCH_IL.0,16_IC1147401_KO17,35.htm?src=GD_JOB_AD&srs=JOBS_HOME_RECENT_SEARCHES&jl=1008504891773&ao=1136043&s=58&guid=00000187cb052718addf92bdba680b03&pos=101&t=SR-JOBS-HR&vt=w&uido=6370B969392800D7D9E2B3D603450E72&cs=1_759d5260&cb=1682738325689&jobListingId=1008504891773&jrtk=3-0-1gv5ga9pn2dui001-1gv5ga9qlghp5800-2b305cd0034cb30a-')
# time.sleep(100)

# checkbox = driver.find_element(
#     By.XPATH, '/html/body/table/tbody/tr/td/div/div[1]/table/tbody/tr/td[1]/div[1]/div/label/input')
# #driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
# checkbox.click()
# recruit_list = []

# country_list = []
# time.sleep(5)

# card = driver.find_element(
#     By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]')
# print(card)
# driver.close()

import requests
from bs4 import BeautifulSoup as bs
from lxml.html import fromstring
from openpyxl import Workbook
from itertools import cycle
import time
from random import choice
from fake_useragent import UserAgent
import sys
from requests.exceptions import ProxyError, SSLError, ConnectTimeout

def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:80]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],i.xpath('.//td[2]/text()')[0]]) # /text빼고도 되는지 확인
            proxies.add(proxy)
    return proxies

headers={
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    'User-Agent':str(UserAgent().chrome)
}
print(headers)

URL = 'https://www.glassdoor.com/Job/san-francisco-ca-front-end-engineer-jobs-SRCH_IL.0,16_IC1147401_KO17,35.htm?src=GD_JOB_AD&srs=JOBS_HOME_RECENT_SEARCHES&jl=1005579680918&ao=1136043&s=58&guid=00000187e08d26caa000e1a1a285f308&pos=102&t=SR-JOBS-HR&vt=w&uido=6370B969392800D7D9E2B3D603450E72&cs=1_dedfd3ac&cb=1683099560090&jobListingId=1005579680918&jrtk=3-0-1gvg8q9ndi9jp801-1gvg8q9o3gfoj800-b1b6fe2d4b485731-'

proxy_server_list=[]
proxy_server_list = list(get_proxies())
print(proxy_server_list)
while True:
    time.sleep(3)
    if (len(proxy_server_list)==0):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<WARNING')
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<EMPTY PROXY LIST')
        break
    proxy = choice(proxy_server_list)
    print(proxy)
    proxies = {'http': proxy,'https': proxy}
    try:
        resp = requests.get(URL, headers=headers, proxies=proxies, verify=False,timeout=5)
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
                'div.css-19txzrf.e14vl8nk0 > div.css-w04er4.e1tk4kwz6 > div.css-1vg6q84.e1tk4kwz4')
            time.sleep(3)
            print(title.text)

            print('===========================COMPANY_NAME============================')
            company_name = soup.select_one(
                'div.css-w04er4.e1tk4kwz6 > div.d-flex.justify-content-between > div')
            time.sleep(3)
            print(company_name.text)

            print('===========================DESCRIPTION============================')
            description = soup.select_one(
                '#JobDesc1005579680918')
            time.sleep(3)
            print(description.text)
            break
    except (ProxyError, SSLError, ConnectTimeout) as e: 
        print('except..')
        proxy_server_list.remove(proxy)    
    
print("DONE...")