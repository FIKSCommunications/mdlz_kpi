#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8
# 4 DP設置台数
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
chqs = obj.getTargetNum(4, posts.month, posts.startdtstr, posts.clientid, posts.year)

#ターゲット店舗取得
shops = obj.getTargetShop(4, posts.startdtstr, posts.clientid, posts.startdtYearmonth, posts.enddtYearmonth)

#サマリー初期値
targetSum = 11936  #ここはCSVから取得
regi = 0
num = 0
result = 0
rate = 0

#ターゲット店舗毎に集計
for row in shops:
    #KPI質問4　回答:ガム、キャンディ、ビスケットのHZカートン什器、HZハンガー什器、SDカートン什器、SDハンガー什器の全合計
    sql = 'SELECT kpa_col1 + kpa_col2 + kpa_col3 + kpa_col4 as sum FROM t_report report '\
        'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
        'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
        'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
        'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 5 '\
        'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
        'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder in(1,2,3) '\
        'WHERE rp_delete = 0 AND rp_done = 1 '\
        'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
        'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
        'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 3'
    rows2 = obj.execQuery(sql, [posts.clientid, row['kts_shopid'], posts.enddtstr, posts.startdtstr])

    if len(rows2) > 0:
        #DP設置台数
        num = num + int(rows2[0]['sum']) + int(rows2[1]['sum']) + int(rows2[2]['sum'])

        if row['clsp_chqid'] in chqs:
            #CHQDP設置台数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + int(rows2[0]['sum']) + int(rows2[1]['sum']) + int(rows2[2]['sum'])

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
