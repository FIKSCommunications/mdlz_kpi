#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8
# 1 HZ占有率
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e

# post値取得 startdt:'2021-02' enddt:'2021-02' clientid:162
posts = inputParser()

# DBaccsess
obj = dbAccessor()

#ターゲット数値取得
sql = 'SELECT ktv_chqid, clcq_name as chq, ktv_month%s as `all`, 0 as regi, 0 as num FROM m_kpi_target_value val '\
        'INNER JOIN t_client_chq ON ktv_chqid = clcq_chqid AND ktv_clientid = clcq_clientid '\
        'WHERE ktv_delete = 0 AND clcq_delete = 0 '\
        'AND clcq_term_1 <= %s AND clcq_term_2 >= %s '\
        'AND ktv_clientid = %s AND ktv_year = %s AND ktv_qno = 1'
rows = obj.execQuery(sql, [posts.month, posts.startdtstr, posts.startdtstr, posts.clientid, posts.year])

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
shops = obj.execQuery(sql, [posts.startdtstr, posts.startdtstr, posts.clientid, posts.startdt, posts.enddt])

#サマリー初期値
regi = 0
num = 0
result = 0

#ターゲット店舗毎に集計
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
    rows2 = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(rows2) > 0:
        #サマリーレジ台数
        regi = regi + int(rows2[0]['kpa_col1'])

        if row['clsp_chqid'] in chqs:
            #CHQレジ台数
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
    rows2 = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(rows2) > 0:
        #サマリー拠点数
        num = num + int(rows2[0]['kpa_col1'])

        if row['clsp_chqid'] in chqs:
            #CHQ拠点数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + int(rows2[0]['kpa_col1'])

#サマリーカバレッジ
if regi > 0:
    result = num / regi * 100
    result = round(result, 2)

#params = {"regi":regi, "num":num, "result":result}
chqs = list(chqs.values())
json_str = json.dumps(chqs, indent=2)

# json出力
h(json_str)
