import pymysql
import requests
import json
from fake_useragent import UserAgent
from lxml.html import fromstring
from itertools import cycle
from random import choice
import datetime

def push_data_to_mysql(datas):

    con = pymysql.connect(
        host='swever2.c996mzyatxge.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='swever123!!',
        charset='utf8',
        db='SWEVER'
        )
    cur = con.cursor()
    for data in datas:
        cur.execute('select count(*) from review where title = %s and link = %s', [data['title'],data['link']])        
        con.commit()
        row =cur.fetchone()[0]

        print(data['title'])
        print(data['link'])
        print(row)
        if (row > 0):
            print('중복된 데이터입니다.')
            continue
    
        thumbnail = ''
        try:
            snippet = data['snippet']
        except:
            snippet = ''
        try:            
            thumbnail = data['pagemap']['cse_thumbnail'][0]['src']
        except:
            thumbnail = ''
        
        cur.execute("insert into review(creator_id, title, link, snippet, thumbnail) values(%s,%s,%s,%s,%s)",\
            [1, data['title'],data['link'],snippet, thumbnail])
        con.commit()
        print("ONE TUPLE IS INSERTED!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
idx=1
key=''
while idx < 100:
    url = f'https://www.googleapis.com/customsearch/v1?q=핀란드 개발자 취업 후기&cx=13448b6eda37544d5&key={key}&start={idx}'    
    idx+=10
    
    # API 요청 보내기
    response = requests.get(url)
    
    data=response.json()
    print("DATA STATUS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(data)

    print(data['items'])
    push_data_to_mysql(data['items'])