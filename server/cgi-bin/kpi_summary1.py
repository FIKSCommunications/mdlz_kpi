#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8
# 1 HZ占有率
import cgi
import sys
from datetime import datetime, date, timedelta
import calendar
import configparser
import MySQLdb
import json
import pprint

form = cgi.FieldStorage()

# 設定ファイル読込
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

# 接続する
#conn = MySQLdb.connect(
#user=config_ini['mysql']['user'],
#passwd=config_ini['mysql']['passwd'],
#host=config_ini['mysql']['host'],
#db=config_ini['mysql']['db'],
#use_unicode=True,
#charset="utf8"
#)
conn = MySQLdb.connect(
user='root',
passwd='admin',
host='localhost',
db='ddss_new_origin',
use_unicode=True,
charset="utf8"
)
cur = conn.cursor()

#月の最終日を求める
def get_last_date2(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])

#引数
#clientid
clientid = 162
#開始日、終了日
startdt = '202101'
enddt = '202101'

#開始日終了日の取得
today = datetime.today()
todaystr = datetime.strftime(today, '%Y-%m-%d')
todayYearmonth = datetime.strftime(today, '%Y%m')
yesterday = today - timedelta(days=1)
yesterdaystr = datetime.strftime(yesterday, '%Y-%m-%d')
yearmonth = datetime.strftime(yesterday, '%Y%m')

#開始日
startdtstr = startdt[0:4] + '-' + startdt[4:6] + '-01'

#終了日
if todayYearmonth == enddt:
    enddtstr = yesterdaystr
else:
    enddtstr = str(get_last_date2(int(enddt[0:4]), int(enddt[4:6])))

#ターゲット店舗取得
sql = 'SELECT kts_shopid FROM m_kpi_target_shop kpi WHERE kts_delete = 0 '\
        'AND kts_clientid = %s AND kts_yearmonth >= %s AND kts_yearmonth <= %s '\
        'AND kts_question1 = 1'
cur.execute(sql, (clientid, startdt, enddt))
rows = cur.fetchall()

regi = 0
kyoten = 0
for row in rows:
    #KPI質問1　回答:レジ台数
    sql = 'SELECT kpa.kpa_col1 FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 1 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= "' + enddtstr + '" '\
        'AND rp_date >= "' + startdtstr + '" ORDER BY rp_date DESC LIMIT 1'
    cur.execute(sql, (clientid, row[0]))
    rows2 = cur.fetchone()
    if rows2 == None:
        continue
    regi = regi + int(rows2[0])

    #KPI質問2　回答:MDLZ製品（ガム、キャンディ、タブ）がある
    sql = 'SELECT kpa.kpa_col1 FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 2 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= "' + enddtstr + '" '\
        'AND rp_date >= "' + startdtstr + '" ORDER BY rp_date DESC LIMIT 1'
    cur.execute(sql, (clientid, row[0]))
    rows2 = cur.fetchone()
    if rows2 == None:
        continue
    kyoten = kyoten + int(rows2[0])

# 接続を閉じる
conn.close

result = kyoten / regi * 100
result = round(result, 2)
params = {"regi":regi, "kyoten":kyoten, "result":result}
json_str = json.dumps(params, indent=2)

# json出力
print('Status: 200 OK')
#print('Content-Type: application/json; charset=utf-8')
print('Content-Type: text/html\nAccess-Control-Allow-Origin: *\n')
print('\n\n')
print(json_str)
print('\n')
