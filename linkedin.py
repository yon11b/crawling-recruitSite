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
con = pymysql.connect(host='127.0.0.1', user='root',
                      password='ddun123!!', db='swever', charset='utf8')
cur = con.cursor()

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

headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    'User-Agent': str(UserAgent().chrome)
}
print(headers)

URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3575359146&geoId=102454443&keywords=singapore%20it%20visa&location=%EC%8B%B1%EA%B0%80%ED%8F%AC%EB%A5%B4&refresh=true'
resp = requests.get(URL)

proxy_server_list = []
proxy_server_list = list(get_proxies())
print(proxy_server_list)
while True:
    proxy = choice(proxy_server_list)
    print(proxy)
    proxies = {'http': proxy, 'https': proxy}
    try:
        resp = requests.get(URL, headers=headers,
                            proxies=proxies, verify=False, timeout=5)
        time.sleep(2)
        print('try..')
        print(resp.status_code)
        if (resp.status_code == "403"):
            print(resp)
        elif str(resp.status_code) == "200":
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
            parser = fromstring(resp.content)
            soup = bs(resp.text, "html.parser")
            time.sleep(10)
            print(soup)
            time.sleep(100)
            print('===========================TITLE============================')
            title = soup.select_one(
                'body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > a > h2')
            time.sleep(30)
            print(title.text)

            print('===========================COMPANY_NAME============================')
            company_name = soup.select_one(
                'body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span:nth-child(1) > a')
            time.sleep(3)
            print(company_name.text)

            print('===========================DESCRIPTION============================')
            description = soup.select_one(
                'body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > div')
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
