from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml.html import fromstring
import re
import requests
import pymysql
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import time
import emoji
from random import choice
from requests.exceptions import ProxyError, SSLError, ConnectTimeout


def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:50]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

# >>> DB 연결
con = pymysql.connect(host='127.0.0.1', user='root',
                      password='ddun123!!', db='swever', charset='utf8')
cur = con.cursor()

while True:
    try:
        proxy_server_list = list(get_proxies())
        proxy = choice(proxy_server_list)
        print(proxy)
        # 프록시 설정- 방법1
        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy": proxy,
        #     "ftpProxy": proxy,
        #     "sslProxy": proxy,
        #     "proxyType": "MANUAL"
        # }

        # 프록시 & fake-useragent 설정- 방법2
        options = Options()
        ua = UserAgent()        
        #options.add_argument('--proxy-server={}'.format(proxy))
        options.add_argument('user-agent={}'.format(ua.random))        
        driver = webdriver.Chrome(options=options, executable_path='D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
        
        URL = 'https://www.linkedin.com/jobs/search?'
        INIT_URL = 'https://www.linkedin.com/jobs/search?keywords=It&location=%EC%8B%B1%EA%B0%80%ED%8F%AC%EB%A5%B4&geoId=102454443&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        driver.get(INIT_URL)
        driver.set_window_size(1500, 800)

        time.sleep(10)
        driver.implicitly_wait(time_to_wait=60)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
        break
    except:
        print('except..')
        proxy_server_list.remove(proxy)
# 각각의 채용공고는 "base-card relative w-full hover~~"라는 동일한 클래스를 사용한다. 
# 따라서 url만 바꿔주고 클래스는 똑같이 이걸로 접근하면 각각의 채용공고애 접근할 수 있다.
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
# 배너 뜨게 하는 url만 추출하기
for i, job in enumerate(jobs_list):
    href = job.find_element(By.TAG_NAME, "a").get_attribute('href')
    # 채용공고 고유 번호는 -와 ? 사이에 있다. (ex: https://sg.linkedin.com/jobs/view/it-manager-at-dyson-3596184368?refId=tOIAHcjQZxm1jx8)
    start = href.find("-") + 1
    end = href.find("?")
    get_jobID = href[start:end].split("-")[-1]
    job_detail_url = URL+'keywords='+KEYWORD+'&location='+LOCATION+'&geoId=102454443'+OFFSET+'&currentJobId='+str(get_jobID) + \
        '&position='+str(i+10)+'&pageNum='+PAGENUM
    print('<<<<<<<<<<<<<<<<<JOB_DETAIL_URL')
    print(job_detail_url)
    job_detail_urls.append(job_detail_url)

RE_COUNT= 0
PASS = 0
job_detail_infos = []

#for detail_url in job_detail_urls:
for i,detail_url in enumerate(job_detail_urls):
    RE_COUNT = 0
    PASS = 0
    driver.get(url=detail_url)
    driver.implicitly_wait(time_to_wait=60)
    while driver.current_url.startswith('https://www.linkedin.com/login/'): # 크롤링 중에 로그인 페이지가 뜬다면
        if RE_COUNT == 20:           # 20번 시도까지 이전 페이지로 돌아갔다가 다시 채용공고 클릭 버튼을 눌러본다.
            PASS = 1                 # 20번이 넘었다면 해당 채용공고는 패스하고 다음 채용공고 크롤링으로 넘어감.
            break
        RE_COUNT = RE_COUNT + 1
        print(f'{RE_COUNT} try....')
        driver.back
        driver.get(url=detail_url)
        driver.implicitly_wait(time_to_wait=60)
    if PASS == 1:
        continue
    print('===========================PRINT-URL============================')
    print(detail_url)
    print('================================================================')
    job_detail_info = []
    time.sleep(5)
    print(1)
    try:
        title = driver.find_element(By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > a > h2")        
        print(2)
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
    except:
        continue

con.close()
driver.close()
