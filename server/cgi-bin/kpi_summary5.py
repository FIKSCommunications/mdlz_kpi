#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8
# 5 大陳数
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
chqs = obj.getTargetNum(5, posts.month, posts.startdtstr, posts.clientid, posts.year)

#ターゲット店舗取得
shops = obj.getTargetShop(5, posts.startdtstr, posts.clientid, posts.startdtYearmonth, posts.enddtYearmonth)

#サマリー初期値
targetSum = 1766  #ここはCSVから取得
regi = 0
num = 0
result = 0
rate = 0

#ターゲット店舗毎に集計
for row in shops:
    #KPI質問6 ガムF数
    sql = 'SELECT kpa_col1 + kpa_col2 as sum FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 6 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 2'
    gum = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(gum) == 2:
        if gum[0]['sum'] >= 10 and gum[0]['sum'] > gum[1]['sum']:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQガムF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1
    elif len(gum) == 1:
        if gum[0]['sum'] >= 10:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQガムF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1
    

    #KPI質問6 キャンディタブF数
    sql = 'SELECT kpa_col1 + kpa_col2 as sum FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 6 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 2 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 2'
    candy = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(candy) == 2:
        if candy[0]['sum'] >= 10 and candy[0]['sum'] > candy[1]['sum']:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQキャンディF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1
    elif len(candy) == 1:
        if candy[0]['sum'] >= 10:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQキャンディF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1




    #KPI質問7 F数
    sql = 'SELECT kpa_col1 + kpa_col2 as sum FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 7 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 2'
    viscuit = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(viscuit) == 2:
        if viscuit[0]['sum'] >= 10 and viscuit[0]['sum'] > viscuit[1]['sum']:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQビスケットF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1
    elif len(viscuit) == 1:
        if viscuit[0]['sum'] >= 10:
            num = num + 1
            if row['clsp_chqid'] in chqs:
                #CHQビスケットF数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + 1

chqs = list(chqs.values())

#達成率の計算
for chq in chqs:
    if chq['all'] > 0:
        chq['rate'] = round((chq['num'] / chq['all']) * 100, 2)

#サマリーカバレッジ、サマリー達成率
if num > 0:
    rate = round(num / targetSum * 100, 2)

#サマリーもJSONに含める
summary = {'all':targetSum, 'regi':regi, 'num':num, 'cavarege':result, 'rate':rate}
response = {'summary': summary, 'detail': chqs}

json_str = json.dumps(response, indent=2)

# json出力
h(json_str)
