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

    #ターゲット数値取得
    def getTargetNum(self, qno, month, startdtstr, clientid, year):
        sql = 'SELECT ktv_chqid, clcq_name as chq, ktv_month%s as `all`, 0 as regi, 0 as num, 0 as cavarege, 0 as rate FROM m_kpi_target_value val '\
                'INNER JOIN t_client_chq ON ktv_chqid = clcq_chqid AND ktv_clientid = clcq_clientid '\
                'WHERE ktv_delete = 0 AND clcq_delete = 0 '\
                'AND clcq_term_1 <= %s AND clcq_term_2 >= %s '\
                'AND ktv_clientid = %s AND ktv_year = %s AND ktv_qno = %s'
        rows = self.execQuery(sql, [month, startdtstr, startdtstr, clientid, year, qno])
        #タプル=>辞書型に変換
        chqs = {}
        for row in rows:
            chqs[row['ktv_chqid']] = dict(row)
        return chqs

    #ターゲット店舗取得
    def getTargetShop(self, qno, startdtstr, clientid, startYearmonth, endYearmonth):
        sql = 'SELECT kts_shopid, clsp_chqid FROM m_kpi_target_shop kpi '\
                'INNER JOIN t_client_shop shop ON kts_shopid = clsp_shopid AND kts_clientid = clsp_clientid '\
                'WHERE kts_delete = 0 AND clsp_delete = 0 '\
                'AND clsp_term_1 <= %s AND clsp_term_2 >= %s '\
                'AND kts_clientid = %s AND kts_yearmonth >= %s AND kts_yearmonth <= %s '\
                'AND kts_question%s = 1 ORDER BY clsp_chqid ASC'
        return self.execQuery(sql, [startdtstr, startdtstr, clientid, startYearmonth, endYearmonth, qno])


    def __del__(self):
        self.conn.close()
