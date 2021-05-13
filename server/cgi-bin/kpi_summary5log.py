#!/usr/bin/python3
# coding: utf-8
# 5 大陳数
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e
import datetime
#import subprocess
      

# post値取得 startdt:'2021-02' enddt:'2021-02' clientid:162 months:['2021-01', '2021-02']
# [{
#   month:1,
#   startdtstr:'2021-01-01',
#   enddtstr:'2021-01-31',
#   clientid:162,
#   year:2021,
#   startdtYearmonth:'202101',
#   enddtYearmonth:'202101'
# }]
posts = inputParser()

#現在時刻
dt_today = datetime.date.today()
dt_now = datetime.datetime.now()
dt_nowstr = dt_now.strftime('%Y-%m-%d %H:%M:%S')

kps_status = 'execute'
kps_searchdt = dt_today
kps_qid = 5
kps_term_1 = posts.startdt
kps_term_2 = posts.enddt
kps_userid = 0
kps_newdate = dt_nowstr

# DBaccsess
obj = dbAccessor()


data = {
    'kps_status': kps_status,
    'kps_searchdt': kps_searchdt,
    'kps_qid': kps_qid,
    'kps_term_1': kps_term_1,
    'kps_term_2': kps_term_2,
    'kps_userid': kps_userid,
    'kps_newdate': kps_newdate,
}

# LOGに存在するかチェック
log = obj.getSearchLog(data)
if log and len(log) == 1:
    logtext = log[0]['KPS_LOG']
    h(logtext)
    sys.exit()

# 検索条件をDBに登録
ret = obj.insertSearchLog(data)

keyid = -1
pid = 0
if (ret):
    sql = "SELECT KPSID FROM t_kpi_searchlog WHERE "\
            "KPS_STATUS = 'execute' AND "\
            "KPS_SEARCHDT = %(kps_searchdt)s AND "\
            "KPS_QID = %(kps_qid)s AND "\
            "KPS_TERM_1 = %(kps_term_1)s AND "\
            "KPS_TERM_2 = %(kps_term_2)s AND "\
            "KPS_USERID = %(kps_userid)s AND "\
            "KPS_NEWDATE = %(kps_newdate)s LIMIT 1"
    row = obj.execQuery(sql, data)
    if len(row) > 0:
        keyid = row[0]['KPSID']

        # subprocess開始
        # command = ['py','kpi_summary5exec.py',posts.startdt,posts.enddt,str(posts.clientid),str(keyid)]
        # command = 'py kpi_summary5exec.py '+posts.startdt+' '+posts.enddt+' '+str(posts.clientid)+' '+str(keyid)
        # proc = subprocess.Popen(command,stdin=None, stdout=None, stderr=None)
        # proc = subprocess.Popen(command)
        # pid = proc.pid


    else:
        ret = False

response = {'result': ret, 'type': '', 'detail': keyid, 'pid': pid}
json_str = json.dumps(response)

if (ret):
    h(json_str)
else:
    e(json_str)
