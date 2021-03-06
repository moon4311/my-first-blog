
import sqlite3
from sqlite3 import Error


class Connector:

    def __init__(self):
        self.db = "test.sqlite3"
        # db = "D://djangogirls/test.sqlite3"

    def show(self):
        print("db : ", self.db)

    def get_db_name(self):
        return self.db

    def set_db_name(self, db):
        self.db = db

    def connect(self):
        return sqlite3.connect(self.db)

    def set_query_column(self, param):
        """
        :param sql:  select , insert into , update 
        :param param: ("id","name","date" ... )
        :return: query
        """
        param_str = ""
        if type(param) == "str":
            param_str = "*"
        else:
            for column in param:
                param_str = param_str + " " + column
                if column != param[len(param)-1]:
                    param_str = param_str + ","
        return param_str

    def set_select_column(self, param):
        """
        :param sql:  select , insert into , update
        :param param: ("id","name","date" ... )
        :return: query
        """
        return "SELECT" + self.set_query_column(param) + " FROM "

    def set_query_param(self, sql, param):
        """
        :param sql:  select ~ from  
        :param param:  {"id" : "1", "name" : "KJM" }
        :return: query
        """
        if param == {}:
            return sql
        else:
            sql = sql + " WHERE "
            while len(param) != 0 :
                column = param.popitem()
                sql = sql + column[0] + " = :"+column[0] + " "
                if len(param) >= 1:
                    sql = sql + " AND "
        return sql

    def select_all(self, table, param, column="*", group=""):
        """
        :param table: Table Name
        :param param: Parameter  ex) {"id":"1", "title":"Test"} or {}
        :param column: ("id","name","data" ...)
        :param group: " a, b, c"
        :return:
        """
        query = self.set_query_param(self.set_select_column(column) + table, param.copy())
        if group != "":
            query = query + " GROUP BY " + group
        return self.select(query, param)

    def select_limit(self, table, param, column="*", group="", order_by="rowId desc", cnt=1):
        """
        :param table: Table Name
        :param param: Parameter  ex) {"id":"1", "title":"Test"}
        :param column: ("id","name","data" ...)
        :param group : "a, b, c"
        :param order_by: column name "id"
        :param cnt: limit count
        :return:
        """
        query = self.set_query_param(self.set_select_column(column) + table, param.copy())
        if group != "":
            query = query + " GROUP BY " + group
        query = query + " ORDER BY " + order_by + " LIMIT " + str(cnt)
        return self.select(query, param)

    def select_latest(self):
        return self.select("SELECT latest FROM result GROUP BY g_id")

    def select_latest_case(self,case):
        query = "SELECT latest FROM result WHERE "
        return self.select("SELECT latest FROM result GROUP BY g_id")

    def select(self, query, param={}):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, param)
        rows = cur.fetchall()
        conn.close()
        return rows

    def insert(self, table, insert_data):
        """
        :param table:  "table Name"
        :param insert_data: {"id":"a", "Title":"ttt"}
        :return: boolean
        """
        conn = self.connect()
        boole = True
        try:
            cur = conn.cursor()
            if type(insert_data) == dict:
                keys = str(tuple(insert_data.keys()))
                values = str(tuple(insert_data.values()))
                query = "INSERT INTO " + table + " " + keys + " VALUES " + values
                cur.execute(query)
            else:
                for data in insert_data:
                    keys = str(tuple(data.keys()))
                    values = str(tuple(data.values()))
                    query = "INSERT INTO " + table + " " + keys + " VALUES " + values
                    cur.execute(query)
            conn.commit()
        except Error as e:
            print("ERROR : ", e)
            boole = False
        finally:
            conn.close()
        return boole
