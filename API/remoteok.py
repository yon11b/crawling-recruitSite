import pymysql
import requests
import json
from fake_useragent import UserAgent
from lxml.html import fromstring
from itertools import cycle
from random import choice
import datetime


def push_data_to_mysql(data):
    
    print(data[1]['slug'])
    
    RECRUIT = data[1]
    print(RECRUIT['slug'])
    print(RECRUIT['date'])
    print(RECRUIT['company'])
    print(RECRUIT['company_logo'])
    print(RECRUIT['position'])
    print(RECRUIT['tags'])
    print(RECRUIT['description'])
    print(RECRUIT['location'])
    print(RECRUIT['salary_max'])
    print(RECRUIT['url'])
    print(RECRUIT['apply_url'])
    
    # string 타입의 date를 UNIX 시간으로 변환
    datetime_obj = datetime.datetime.strptime(RECRUIT['date'], '%Y-%m-%dT%H:%M:%S%z')    
    unix_time = int(datetime_obj.timestamp())
    print(unix_time)
    
    # tags를 하나의 string으로 변환
    tags_string = ' '.join(RECRUIT['tags'])
    
    print("======================================================")
    con = pymysql.connect(
        host='database-1.cgy1torosydx.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='swever123!!',

        charset='utf8',
        db='SWEVER'
        )
    cur = con.cursor()
    print('===================')
    cur.execute("INSERT INTO RECRUIT_POST(\
        NATION_ID, COMPANY_NAME, DESCRIPTION_TITLE, DESCRIPTION_CONTENT, COMPANY_APPLY_LINK, POSTED_DATE,\
        IS_VISA_SPONSORED, IS_REMOTED, COMPANY_LOGO, SALARY, CONTRACT_FORM, COMPANY_PAGE_LINK,\
        WRITER, ORIGIN, TAG, LOCATION, IS_DEV\
        )\
        VALUES(%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s)",
        [0,RECRUIT['company'],RECRUIT['slug'],RECRUIT['description'],RECRUIT['apply_url'], unix_time,\
        '0', '1', RECRUIT['logo'], RECRUIT['salary_max'],RECRUIT['position'],RECRUIT['url'],\
        'Swever','remoteok.com', tags_string, RECRUIT['location'],'1'])
    con.commit()


def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
headers={
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    'User-Agent':str(UserAgent().chrome)
}

url = 'https://remoteok.com/api?api=1'

proxy_server_list=[]
proxy_server_list = list(get_proxies())
print(proxy_server_list)
while True:
    if (len(proxy_server_list)==0):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<WARNING')
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<EMPTY PROXY LIST')
        break
    proxy = choice(proxy_server_list)
    print(proxy)
    proxies = {'http': proxy,'https': proxy}
    try:
        # API 요청 보내기
        response = requests.post(url, headers=headers, proxies=proxies, timeout=5)
        print(response.status_code)
        data=response.json()
        push_data_to_mysql(data)
        break
    except pymysql.err.InternalError as e:
        code, msg = e.args
        print(msg)
    except Exception as e:
        print(e)
