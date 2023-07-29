from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import time
from random import choice
from dbconnect import connect_db
from proxies import get_proxies


# 1. Proxy & Fake-useragent 설정
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
        INIT_URL = 'https://www.linkedin.com/jobs/search?keywords=Backend&location=netherlands&geoId=102890719'
        driver.get(INIT_URL)
        driver.set_window_size(1500, 800)
        driver.implicitly_wait(time_to_wait=60)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SUCCESS!!")
        break
    except:
        print('except..')
        proxy_server_list.remove(proxy)

# 2. Database 연결
con, cur = connect_db()

# 3. VARIRABLES
KEYWORD = 'backend'
LOCATION = 'netherlands'
OFFSET = '&trk=public_jobs_jobs-search-bar_search-submit'
PAGENUM = '0'
# GEOID = '102454443'  # 나라 고유 번호- 싱가포르
GEOID = '102890719'    # 나라 고유 번호- 네덜란드
POSITIONS = ['it','developer','unity','infra','database'
    'frontend', 'backend', 'full stack',
             'mobile', 'devops', 'data science', 'security', 'gaming', 'pm',
             'systems engineer', 'network', 'machine learning', 'big data', 'forensic', 'embedded']

# 4. 검색어창에 입력할 직무들: for문
for pos in POSITIONS:
    search_keywords = driver.find_element(By.CSS_SELECTOR, "#job-search-bar-keywords")
    search_keywords.clear()
    search_keywords.send_keys(pos)
    search_keywords.send_keys(Keys.RETURN)
    KEYWORD = pos
    time.sleep(5)
    
    while True:
        # 각각의 채용공고는 "base-card relative w-full hover~~"라는 동일한 클래스를 사용한다. 
        # 따라서 url만 바꿔주고 클래스는 똑같이 이걸로 접근하면 각각의 채용공고애 접근할 수 있다.
        jobs_list = driver.find_elements(
            By.CSS_SELECTOR, "div.base-card.relative.w-full.hover\:no-underline.focus\:no-underline.base-card--link.base-search-card.base-search-card--link.job-search-card")

        job_detail_urls = []
        # 배너 뜨게 하는 url만 추출하기
        for i, job in enumerate(jobs_list):
            href = job.find_element(By.TAG_NAME, "a").get_attribute('href')
            # 채용공고 고유 번호는 -와 ? 사이에 있다. (ex: https://sg.linkedin.com/jobs/view/it-manager-at-dyson-3596184368?refId=tOIAHcjQZxm1jx8)
            start = href.find("-") + 1
            end = href.find("?")
            get_jobID = href[start:end].split("-")[-1]
            job_detail_url = URL+'keywords='+KEYWORD+'&location='+LOCATION+'&geoId='+GEOID+OFFSET+'&currentJobId='+str(get_jobID) + \
                '&position='+str(i+10)+'&pageNum='+PAGENUM
            print('<<<<<<<<<<<<<<<<<JOB_DETAIL_URL')
            print(job_detail_url)
            job_detail_urls.append(job_detail_url)

        RE_COUNT= 0
        PASS = 0
        job_detail_infos = []

        for detail_url in job_detail_urls:
            URL = detail_url
            RE_COUNT = 0
            PASS = 0
            driver.get(url=detail_url)
            driver.implicitly_wait(time_to_wait=60)
           
            print('===========================PRINT-URL============================')
            print(detail_url)
            print('================================================================')
            job_detail_info = []
            time.sleep(5)
            # 크롤링 중에 로그인 페이지가 뜬다면
            while driver.current_url.startswith('https://www.linkedin.com/login/'):
                if RE_COUNT == 20:           # 20번 시도까지 이전 페이지로 돌아갔다가 다시 채용공고 클릭 버튼을 눌러본다.
                    # 20번이 넘었다면 해당 채용공고는 패스하고 다음 채용공고 크롤링으로 넘어감.
                    PASS = 1
                    break
                RE_COUNT = RE_COUNT + 1
                print(f'{RE_COUNT} try....')
                driver.back
                driver.get(url=detail_url)
                driver.implicitly_wait(time_to_wait=60)
            if PASS == 1:
                continue
            try:
                title = driver.find_element(By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > a > h2")        
                title = title.text
                print('===========================TITLE============================')
                print(title)
                job_detail_info.append(title)

                company_name = driver.find_element(
                    By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(1) > span:nth-child(1) > a")
                print('===========================COMPANY_NAME============================')
                company_name = company_name.text
                print(company_name)
                job_detail_info.append(company_name)

                description = driver.find_element(
                    By.CSS_SELECTOR, "body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > div > section.core-section-container.my-3.description > div")
                print('===========================DESCRIPTION============================')
                description = description.text
                print(description)
                job_detail_info.append(description)
                job_detail_infos.append(job_detail_info)
                #print(job_detail_infos)
                
                print(">>>>>>>>>>>>>>>>>>>>>TYPE PRINT!!<<<<<<<<<<<<<<<<<<<<")
                print(type(title))
                print(type(company_name))
                print(type(description))
                
                #description="test"
                insert_query = "INSERT INTO job_recruit (title, company, position, location, description) VALUES (%s,%s,%s,%s,%s);"
                data = (title, company_name, pos, "netherlands", description)

                cur.execute(insert_query,data)
                con.commit()
            except:
                continue
        driver.get(URL)
    
cur.close()
con.close()
driver.close()