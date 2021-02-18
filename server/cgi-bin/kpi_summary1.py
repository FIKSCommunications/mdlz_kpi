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
chqs = obj.getTargetNum(1, posts.month, posts.startdtstr, posts.clientid, posts.year)

#ターゲット店舗取得
shops = obj.getTargetShop(1, posts.startdtstr, posts.clientid, posts.startdtYearmonth, posts.enddtYearmonth)

#サマリー初期値
targetSum = 35.8  #ここはCSVから取得
regi = 0
num = 0
result = 0
rate = 0

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


chqs = list(chqs.values())

#カバレッジ、達成率の計算
for chq in chqs:
    #targetSum = targetSum + chq['all']
    if chq['regi'] > 0:
        chq['cavarege'] = round((chq['num'] / chq['regi']) * 100, 2)
    if chq['all'] > 0:
        chq['rate'] = round((chq['cavarege'] / chq['all']) * 100, 2)

#サマリーカバレッジ、サマリー達成率
if regi > 0:
    result = round(num / regi * 100, 2)
if result > 0:
    rate = round(result / targetSum * 100, 2)

#サマリーもJSONに含める
summary = {'all':35.8, 'regi':regi, 'num':num, 'cavarege':result, 'rate':rate}
response = {'summary': summary, 'detail': chqs}

json_str = json.dumps(response, indent=2)

# json出力
h(json_str)
