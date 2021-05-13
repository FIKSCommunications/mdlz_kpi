#!/usr/bin/python3
# coding: utf-8
# 5 大陳数完了Cronチェック
import sys
from dbAccessor import dbAccessor
import datetime
import subprocess
      
#コマンドライン引数があればkeyidとして実行、無ければ当日一番最初の対象を実行
args = sys.argv

keyid = -1
if len(args) == 2 and args[1].isdigit():
    keyid = int(args[1])

dt_today = datetime.date.today()

# DBaccsess
obj = dbAccessor()

if (keyid == -1):
    sql = "SELECT KPSID, KPS_STATUS, KPS_SEARCHDT, KPS_QID, KPS_TERM_1, KPS_TERM_2 FROM t_kpi_searchlog WHERE "\
            "KPS_DELETE = 0 AND KPS_STATUS = 'execute' AND KPS_QID = 5 AND KPS_SEARCHDT = %s AND KPS_LOG IS NULL "\
            "LIMIT 1"
    rows = obj.execQuery(sql,[dt_today])
else:
    sql = "SELECT KPSID, KPS_STATUS, KPS_SEARCHDT, KPS_QID, KPS_TERM_1, KPS_TERM_2 FROM t_kpi_searchlog WHERE KPSID = %s"
    rows = obj.execQuery(sql,[keyid])

if len(rows) == 1:
    #作業中フラグを立てる
    upid = rows[0]['KPSID']
    upsql = "UPDATE t_kpi_searchlog SET KPS_STATUS = 'cron' WHERE KPSID = %s"
    obj.cur.execute(upsql, [upid])
    obj.conn.commit()

    #実際の処理実行
    print('exec start')
    subprocess.run(['py','kpi_summary5exec.py',rows[0]['KPS_TERM_1'],rows[0]['KPS_TERM_2'],'162',str(upid)])
    print('exec end')

sys.exit()
