#!/usr/bin/python3
# coding: utf-8
# 1 HZ占有率
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e, int2

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

# DBaccsess
obj = dbAccessor()

#複数月合計用
gTargetSum = 0
gTargetRegi = 0
gTargetKyoten = 0
gRegi = 0
gNum = 0
gResult = 0
gRate = 0
gChqs = {}

for mon in posts.months:

    #print(mon)

    #ターゲット数値取得
    chqs = obj.getTargetNum(1, mon['month'], mon['startdtstr'], mon['clientid'], mon['year'])

    #ターゲット店舗取得
    shops = obj.getTargetShop(1, mon['startdtstr'], mon['clientid'], mon['startdtYearmonth'], mon['enddtYearmonth'])

    #サマリー初期値
    targetRegi = obj.getAllTargetNum(0, mon['month'], mon['clientid'], mon['year'])
    targetKyoten = obj.getAllTargetNum(1, mon['month'], mon['clientid'], mon['year'])

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
        rows2 = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        if len(rows2) > 0:
            #サマリーレジ台数
            regi = regi + int2(rows2[0]['kpa_col1'])

            if row['clsp_chqid'] in chqs:
                #CHQレジ台数
                chqs[row['clsp_chqid']]['regi'] = chqs[row['clsp_chqid']]['regi'] + int2(rows2[0]['kpa_col1'])

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
        rows2 = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        if len(rows2) > 0:
            #サマリー拠点数
            num = num + int2(rows2[0]['kpa_col1'])

            if row['clsp_chqid'] in chqs:
                #CHQ拠点数
                chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + int2(rows2[0]['kpa_col1'])

        #shop毎ここまで

    #chqs カバレッジ、達成率の計算
    for k, v in chqs.items():
        if k in gChqs:
            gChqs[k]['regi'] += v['regi']
            gChqs[k]['num'] += v['num']
        else:
            gChqs[k] = v

    #gTargetSum += targetSum
    gRegi += regi
    gNum += num

    # 月のレジ台数、拠点数の累計
    gTargetRegi = gTargetRegi + targetRegi
    gTargetKyoten = gTargetKyoten + targetKyoten

    #月ループ　ここまで


#月を含めた全集計

#全企業ターゲット占有率
if gTargetRegi > 0:
    gTargetSum = round(gTargetKyoten / gTargetRegi * 100, 2)

#gTargetSum = gTargetSum / len(posts.months)
if gRegi > 0:
    gResult = round(gNum / gRegi * 100, 2)
if gTargetSum > 0:
    gRate = round(gResult / gTargetSum * 100, 2)

#chq別のカバレッジ、達成率
gChqs = list(gChqs.values())

for gchq in gChqs:
    if gchq['regi'] > 0:
        gchq['cavarege'] = round(gchq['num'] / gchq['regi'] * 100, 2)
    if gchq['all'] > 0:
        gchq['rate'] = round(gchq['cavarege'] / gchq['all'] * 100, 2)

#サマリーもJSONに含める
summary = {'all':gTargetSum, 'regi':gRegi, 'num':gNum, 'cavarege':gResult, 'rate':gRate}
response = {'summary': summary, 'detail': gChqs}
json_str = json.dumps(response, indent=2)

# json出力
h(json_str)
