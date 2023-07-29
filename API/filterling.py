import csv
import pymysql

# CSV 파일에서 도시-국가 매칭 후, 국가 정보를 DB에 삽입

def push_data_to_mysql(datas):

    con = pymysql.connect(
        host='database-1.cgy1torosydx.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='swever123!!',

        charset='utf8',
        db='SWEVER'
        )
    cur = con.cursor()
    cur.execute("SELECT INTO RECRUIT_POST(\
        NATION_ID, COMPANY_NAME, DESCRIPTION_TITLE, DESCRIPTION_CONTENT, COMPANY_APPLY_LINK, POSTED_DATE,\
        IS_VISA_SPONSORED, IS_REMOTED, COMPANY_LOGO, SALARY, CONTRACT_FORM, COMPANY_PAGE_LINK,\
        WRITER, ORIGIN, TAG, LOCATION, IS_DEV\
        )\
        VALUES(%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s)",
        [0,data['company'],data['slug'],data['description'],data['apply_url'], unix_time,\
        '0', '1', data['logo'], data['salary_max'],data['position'],data['url'],\
        'Swever','remoteok.com', tag_string, data['location'],'1'])
    con.commit()
    print("ONE TUPLE IS INSERTED!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")




file = open('worldcity.csv', 'r')
# CSV 파일 읽기
reader = csv.reader(file)

# 헤더 제외한 데이터만 읽기
next(reader)  # 첫 번째 행(헤더)을 건너뜀

# A열 데이터 출력
for row in reader:
    a_data = row[0]  # A열 데이터
    print(a_data)
    break
file.close()

