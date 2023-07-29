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
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:30]:
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

URL = 'https://www.linkedin.com/jobs/search?'
INIT_URL = 'https://www.linkedin.com/jobs/search?keywords=It&location=%EC%8B%B1%EA%B0%80%ED%8F%AC%EB%A5%B4&geoId=102454443&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

resp = requests.get(INIT_URL)
soup = bs(resp.text, "html.parser")
jobs_list = soup.select(
    "div.base-card.relative.w-full.hover\:no-underline.focus\:no-underline.base-card--link.base-search-card.base-search-card--link.job-search-card")

# VARIRABLES
KEYWORD = 'it'
LOCATION = 'singapore'
OFFSET = '&trk=public_jobs_jobs-search-bar_search-submit'
PAGENUM = '0'
GEOID = '102454443'  # 나라 고유 번호?
job_detail_urls = []
# 배너 뜨게 하는 url만 추출하기
for i, job in enumerate(jobs_list):
    href = job.select_one('a')
    href = href['href']
    start = href.find("-") + 1
    end = href.find("?")
    get_jobID = href[start:end].split("-")[-1]      # 처음 나오는 숫자를 추출
    job_detail_url = URL+'keywords='+KEYWORD+'&location='+LOCATION+'&geoId=102454443'+OFFSET+'&currentJobId='+str(get_jobID) + \
        '&position='+str(i+1)+'&pageNum='+PAGENUM
    print('<<<<<<<<<<<<<<<<<JOB_DETAIL_URL')
    print(job_detail_url)
    job_detail_urls.append(job_detail_url)

proxy_server_list = []
proxy_server_list = list(get_proxies())
print(proxy_server_list)
while True:
    proxy = choice(proxy_server_list)
    print(proxy)
    proxies = {'http': proxy, 'https': proxy}
    try:
        for detail_url in job_detail_urls:
            resp = requests.get(detail_url, headers=headers,
                                proxies=proxies, verify=False, timeout=5)            
            print('try..')
            print(resp.text)
            time.sleep(20)
            if (resp.status_code == "403"):
                print(resp)
            elif str(resp.status_code) == "200":
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
                parser = fromstring(resp.content)
                time.sleep(10)
                #print(soup)
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
