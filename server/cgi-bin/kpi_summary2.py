#!/usr/bin/python3
# coding: utf-8
# 1 HZ占有率
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e

# post値取得 startdt:'2021-02' enddt:'2021-02' clientid:162
posts = inputParser()

#複数月合計用
gTargetSum = 0
gNum = 0
gRate = 0
gChqs = {}

# DBaccsess
obj = dbAccessor()

for mon in posts.months:
    
    #print(mon)

    #ターゲット数値取得
    chqs = obj.getTargetNum(2, mon['month'], mon['startdtstr'], mon['clientid'], mon['year'])

    #ターゲット店舗取得
    shops = obj.getTargetShop(2, mon['startdtstr'], mon['clientid'], mon['startdtYearmonth'], mon['enddtYearmonth'])

    #サマリー初期値
    targetSum = obj.getAllTargetNum(2, mon['month'], mon['clientid'], mon['year'])
    num = 0
    rate = 0

    #ターゲット店舗毎に集計
    for row in shops:
        #KPI質問2　回答:MDLZ製品（ガム、キャンディ、タブ）がある
        sql = 'SELECT kpa_col1 FROM t_report report '\
            'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
            'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
            'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
            'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 3 '\
            'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
            'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 1'
        rows2 = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        if len(rows2) > 0:
            #展開面数
            num = num + 1

            if row['clsp_chqid'] in chqs:
                #CHQ拠点数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + int(rows2[0]['kpa_col1'])

        #shop毎ここまで

    #chqs 達成率の計算
    for k, v in chqs.items():
        if k in gChqs:
            gChqs[k]['all'] += v['all']
            gChqs[k]['num'] += v['num']
        else:
            gChqs[k] = v

    gTargetSum += targetSum
    gNum += num

    #月ループ　ここまで
    #chqs = list(chqs.values())

#月を含めた全集計
#gTargetSum = gTargetSum / len(posts.months)
if gTargetSum > 0:
    gRate = round(gNum / gTargetSum * 100, 2)

#chq別達成率
gChqs = list(gChqs.values())

for gchq in gChqs:
    if gchq['all'] > 0:
        gchq['rate'] = round(gchq['num'] / gchq['all'] * 100, 2)

#サマリーもJSONに含める
summary = {'all':gTargetSum, 'num':gNum,  'rate':gRate}
response = {'summary': summary, 'detail': gChqs}

json_str = json.dumps(response, indent=2)

# json出力
h(json_str)
