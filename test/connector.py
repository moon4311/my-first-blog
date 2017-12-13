
import sqlite3
from sqlite3 import Error

# db = "test.sqlite3"
# db = "D://djangogirls/test.sqlite3"
db = "../db.sqlite3"


def get_database():
    print("get_database : ", db)
    return db


def set_database(db):
    super.db = db


def connect():
    print("connect db : ", db)
    return sqlite3.connect(get_database())



def setting_query(sql,param):
    while len(param) != 0 :
        column = param.popitem()
        sql = sql + column[0] + " = :"+column[0] + " "
        if len(param) >= 1 : sql = sql + " AND "
    print("query : " , sql)
    return sql

def select_All(table,param) :
    """
    :param table: Table Name
    :param param: Parameter  ex) (1,'sea')
    :return:
    """
    conn = connect()
    sql = " SELECT * FROM " + table + " WHERE "
    c_param = param.copy()
    sql = setting_query(sql,c_param)
    cur = conn.cursor()
    cur.execute(sql,param)
    rows = cur.fetchall()
    conn.close()
    return rows

def select_All(table,column,param) :
    """
    :param table: Table Name
    :param param: Parameter  ex) (1,'sea')
    :return:
    """
    conn = connect()


    sql = " SELECT "
    
    ########################################column

    c_param = param.copy()
    sql = setting_query(sql,c_param)
    cur = conn.cursor()
    cur.execute(sql,param)
    rows = cur.fetchall()
    conn.close()
    return rows



rows = select_All("blog_post", {'id':'1','text':'Test'})
print(rows)

def insert_result(table,insert_data):
    conn = sqlite3.connect(db)
    sql =  "insert into result(g_id, sequence,result,ex_o,ex_e,o,e,t,img ) " + " "