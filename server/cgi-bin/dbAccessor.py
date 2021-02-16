#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8
import MySQLdb
from MySQLdb.cursors import DictCursor

class dbAccessor:

    def __init__(self):
        self.conn = MySQLdb.connect(
            user='root',
            passwd='admin',
            host='localhost',
            db='ddss_new_origin',
            use_unicode=True,
            charset="utf8"
        )
        self.cur = self.conn.cursor(DictCursor)
    
    def execQuery(self, sql, bind):
        self.cur.execute(sql, bind)
        rows = self.cur.fetchall()
        return rows
    
    def __del__(self):
        self.conn.close()
