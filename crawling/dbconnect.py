import time
import psycopg2

def connect_db():
    try:
        # >>> DB 연결 [MYSQL]
        # con = pymysql.connect(host='127.0.0.1', user='root', password='ddun123!!', db='swever', charset='utf8')
        
        # >>> DB 연결 [POSTGRESQL]
        con = psycopg2.connect(host='127.0.0.1', user='postgres',
                            password='ddun123!!', database='swever')        
        print("DATABASE CONNECT SUCCESSFULL!!")
    except psycopg2.DatabaseError as e:
        print(e)
        exit()
    cur = con.cursor()
    return con, cur