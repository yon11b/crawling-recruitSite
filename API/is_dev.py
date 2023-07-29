import pymysql
import requests
import json
from fake_useragent import UserAgent
from lxml.html import fromstring
from itertools import cycle
from random import choice
import datetime

# DB 연결 함수
def connect_DB():
    con = pymysql.connect(
        host='swever2.c996mzyatxge.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='swever123!!',
        charset='utf8',
        db='SWEVER'
        )
    return con

# tech_stack 파이썬 자료형으로 변환하는 함수
def get_tech_stack_dict_list(con):
    cur = con.cursor()    
    cur.execute('select tech_name from tech_stack')
    results = cur.fetchall()
        
    tech_list=[]    
    for result in results:
        json_data = result[0]
        tech = json.loads(json_data)            
        tech_list.append(tech)        
    return tech_list

# 제목을 단어 단위로 쪼개서 IT가 있는지 확인하는 함수
def refined_title(title_data, tag_data):
    ref1 = title_data.replace('-',' ').split()    
    if 'it' in ref1:
        return 1
    return 0

# is_dev 값 수정 함수
def update_dev(con, dev_data, id):
    cur = con.cursor()
    query = 'update recruit_post set is_dev='+dev_data+' where id='+id
    print(query)
    cur.execute(query)
    con.commit()
    return True

# DB에 있는 json 데이터들을 파이썬의 dict 배열(tech_list)로 변환하여 리턴
con = connect_DB()
tech_list = get_tech_stack_dict_list(con)

# 채용공고들의 content와 tag를 순회하여 tech_list의 값과 일치하는 키워드가 있다면 recruit_post의 is_dev값을 1로 수정(없으면 0으로 수정)
# 채용공고의 content와 tag를 불러온다.
cur = con.cursor()
cur.execute('select id, description_title, tag from recruit_post')
tuples = cur.fetchall()
cnt = 0
for tuple in tuples:  
    dev_data = "0"  
    id = str(tuple[0])    
    title = tuple[1]    
    tag = json.loads(tuple[2])    
    tag_data = set(word.lower() for word in tag)
    title_data = title.lower()
    
    for tech in tech_list:  
        tech_data = set(word.lower() for word in tech['data'])        
        tag_intersection = tag_data.intersection(tech_data)        
        
        if tag_intersection:    # 얘만 했을 때는 574개가 dev=1로 분류됨 / (dev=0는 1454개)
            print("THIS IS DEV RECRUIT!!!!")
            dev_data = "1"
            print(id)
            cnt +=1            
        elif "it" in tag_data:
            dev_data = "1"
            cnt += 1
            print('============================================================================================')
        # 'it' 처리. 단어 속에 it가 들어가 있는 경우는 제외하기 위해 단어별로 분리하여 리스트에 넣고 
        # 원소중에 'it'와 일치하는 것이 있다면 dev_data=1로 설정하도록 하였음
        elif refined_title(title_data, tag_data):
            dev_data = "1"
            cnt += 1
        else:
            for tech_atom in tech_data:                
                if tech_atom in title_data:         
                    print(title_data)
                    dev_data = "1"
                    cnt +=1
                    break
        if dev_data=="1":
            break
    update_dev(con, dev_data, id)
print(cnt)