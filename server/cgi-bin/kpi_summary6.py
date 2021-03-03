#!/usr/bin/python3
# coding: utf-8
# 1 HZ占有率
import cgi
import sys
from datetime import datetime, date, timedelta
import calendar
import json
import pprint
from dbAccessor import dbAccessor

form = cgi.FieldStorage()

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

#開始年、開始月
year = startdt[0:4]
month = int(startdt[4:6])


#ターゲット数値取得
sql = 'SELECT ktv_chqid, clcq_name as chqname, ktv_month%s as target, 0 as regi, 0 as kyoten FROM m_kpi_target_value val '\
        'INNER JOIN t_client_chq ON ktv_chqid = clcq_chqid AND ktv_clientid = clcq_clientid '\
        'WHERE ktv_delete = 0 AND clcq_delete = 0 '\
        'AND clcq_term_1 <= %s AND clcq_term_2 >= %s '\
        'AND ktv_clientid = %s AND ktv_year = %s AND ktv_qno = 1'
obj = dbAccessor()
rows = obj.execQuery(sql, [month, startdtstr, startdtstr, clientid, year])
#タプル=>辞書型に変換
chqs = {}
for row in rows:
    chqs[row['ktv_chqid']] = dict(row)


#ターゲット店舗取得
sql = 'SELECT kts_shopid, clsp_chqid FROM m_kpi_target_shop kpi '\
        'INNER JOIN t_client_shop shop ON kts_shopid = clsp_shopid AND kts_clientid = clsp_clientid '\
        'WHERE kts_delete = 0 AND clsp_delete = 0 '\
        'AND clsp_term_1 <= %s AND clsp_term_2 >= %s '\
        'AND kts_clientid = %s AND kts_yearmonth >= %s AND kts_yearmonth <= %s '\
        'AND kts_question1 = 1 ORDER BY clsp_chqid ASC'
shops = obj.execQuery(sql, [startdtstr, startdtstr, clientid, startdt, enddt])

regi = 0
kyoten = 0

for row in shops:
    #KPI質問1　回答:レジ台数
    sql = 'SELECT kpa_col1 FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 1 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 1'
    rows2 = obj.execQuery(sql, [clientid, row['kts_shopid'], enddtstr, startdtstr])
    if len(rows2) > 0:
        regi = regi + int(rows2[0]['kpa_col1'])
        if row['clsp_chqid'] in chqs:
            chqs[row['clsp_chqid']]['regi'] = chqs[row['clsp_chqid']]['regi'] + int(rows2[0]['kpa_col1'])

    #KPI質問2　回答:MDLZ製品（ガム、キャンディ、タブ）がある
    sql = 'SELECT kpa_col1 FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 2 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 1'
    rows2 = obj.execQuery(sql, [clientid, row['kts_shopid'], enddtstr, startdtstr])
    if len(rows2) > 0:
        kyoten = kyoten + int(rows2[0]['kpa_col1'])
        if row['clsp_chqid'] in chqs:
            chqs[row['clsp_chqid']]['kyoten'] = chqs[row['clsp_chqid']]['kyoten'] + int(rows2[0]['kpa_col1'])

#result = 0
#if regi > 0:
#    result = kyoten / regi * 100
#    result = round(result, 2)

#params = {"regi":regi, "kyoten":kyoten, "result":result}
json_str = json.dumps(chqs, indent=2)

# json出力
print('Status: 200 OK')
print('Content-Type: text/html\nAccess-Control-Allow-Origin: *\n')
print('\n\n')
print(json_str)
print('\n')
