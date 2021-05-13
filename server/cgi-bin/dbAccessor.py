#!/usr/bin/python3
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

    #全体ターゲット数値取得
    def getAllTargetNum(self, qno, month, clientid, year):
        sql = 'SELECT ktav_month%s as `all` FROM m_kpi_target_all_value val '\
                'WHERE ktav_delete = 0  '\
                'AND ktav_clientid = %s AND ktav_year = %s AND ktav_qno = %s'
        rows = self.execQuery(sql, [month, clientid, year, qno])
        #タプル=>辞書型に変換
        res = 0
        for row in rows:
            res = row['all']
        return res

    #ターゲット店舗取得
    def getTargetShop(self, qno, startdtstr, clientid, startYearmonth, endYearmonth):
        sql = 'SELECT kts_shopid, clsp_chqid FROM m_kpi_target_shop kpi '\
                'INNER JOIN t_client_shop shop ON kts_shopid = clsp_shopid AND kts_clientid = clsp_clientid '\
                'WHERE kts_delete = 0 AND clsp_delete = 0 '\
                'AND clsp_term_1 <= %s AND clsp_term_2 >= %s '\
                'AND kts_clientid = %s AND kts_yearmonth >= %s AND kts_yearmonth <= %s '\
                'AND kts_question%s = 1 ORDER BY clsp_chqid ASC'
        return self.execQuery(sql, [startdtstr, startdtstr, clientid, startYearmonth, endYearmonth, qno])
    
    #ターゲット商品取得
    def getTargetItem(self, clientid, date):
        sql = 'SELECT ktp_product, ktp_kechakune * ktp_quantity_per_box as price FROM m_kpi_target_product kpi '\
                'WHERE ktp_delete = 0 AND ktp_clientid = %s AND ktp_term_1 <= %s AND ktp_term_2 >= %s '\
                'ORDER BY ktpid ASC'
        return self.execQuery(sql, [clientid, date, date])

    def insertSearchLog(self, data):
        try:
            sql = 'INSERT INTO t_kpi_searchlog (KPS_STATUS,KPS_SEARCHDT,KPS_QID,KPS_TERM_1,KPS_TERM_2,KPS_USERID,KPS_NEWDATE) '\
                'VALUES (%(kps_status)s,%(kps_searchdt)s,%(kps_qid)s,%(kps_term_1)s,%(kps_term_2)s,%(kps_userid)s,%(kps_newdate)s)'
            self.cur.execute(sql, data)
            self.conn.commit()
            return True
        except MySQLdb.Error as e:
            #print('MySQLdb.Error: ', e)
            return False

    def updateSearchLog(self, data):
        try:
            sql = 'UPDATE t_kpi_searchlog SET '\
                'KPS_STATUS = "done",'\
                'KPS_EDITDATE = %(kps_editdate)s,'\
                'KPS_LOG = %(kps_log)s '\
                'WHERE KPSID = %(kpsid)s'
            self.cur.execute(sql, data)
            self.conn.commit()
            return True
        except MySQLdb.Error as e:
            #print('MySQLdb.Error: ', e)
            return False
    
    def checkSearchLog(self, keyid):
        try:
            sql = 'SELECT KPS_LOG FROM t_kpi_searchlog '\
                'WHERE KPSID = %s AND '\
                'KPS_DELETE = 0 AND '\
                'KPS_STATUS = "done"'
            return self.execQuery(sql, [keyid])
        except MySQLdb.Error as e:
            return False
    
    def getSearchLog(self, data):
        try:
            sql = "SELECT KPSID,KPS_LOG FROM t_kpi_searchlog WHERE "\
                    "KPS_DELETE = 0 AND KPS_STATUS = 'done' AND "\
                    "KPS_SEARCHDT = %(kps_searchdt)s AND "\
                    "KPS_QID = %(kps_qid)s AND "\
                    "KPS_TERM_1 = %(kps_term_1)s AND "\
                    "KPS_TERM_2 = %(kps_term_2)s AND "\
                    "KPS_LOG is not NULL LIMIT 1"
            return self.execQuery(sql, data)
        except MySQLdb.Error as e:
            return False

    def __del__(self):
        self.conn.close()
