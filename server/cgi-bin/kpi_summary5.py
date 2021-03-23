#!/usr/bin/python3
# coding: utf-8
# 5 大陳数
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e, int2

def displayCalc(lists):
    ret = 0
    pre = 0
    for i in lists:
        num = int2(i)
        if num >= 10 and num > pre:
            ret += 1
        pre = num
    return ret
        
 
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
gRegi = 0
gNum = 0
gResult = 0
gRate = 0
gChqs = {}

for mon in posts.months:

    #ターゲット数値取得
    chqs = obj.getTargetNum(5, mon['month'], mon['startdtstr'], mon['clientid'], mon['year'])

    #ターゲット店舗取得
    shops = obj.getTargetShop(5, mon['startdtstr'], mon['clientid'], mon['startdtYearmonth'], mon['enddtYearmonth'])

    #サマリー初期値
    targetSum = obj.getAllTargetNum(5, mon['month'], mon['clientid'], mon['year'])

    regi = 0
    num = 0
    result = 0
    rate = 0

    #ターゲット店舗毎に集計
    for row in shops:
        #KPI質問6 ガムF数
        sql = 'SELECT kpa_col1,kpa_col2 FROM t_report report '\
            'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
            'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
            'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
            'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 6 '\
            'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
            'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s ORDER BY rp_date ASC'
        gum = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        listsHZ = [d.get('kpa_col1') for d in gum]
        ret = displayCalc(listsHZ)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQガムF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        listsSD = [d.get('kpa_col2') for d in gum]
        ret = displayCalc(listsSD)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQガムF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        """
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
        """        

        #KPI質問6 キャンディタブF数
        sql = 'SELECT kpa_col1, kpa_col2 FROM t_report report '\
            'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
            'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
            'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
            'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 6 '\
            'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
            'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 2 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s ORDER BY rp_date ASC'
        candy = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        listsHZ = [d.get('kpa_col1') for d in candy]
        ret = displayCalc(listsHZ)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQキャンディF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        listsSD = [d.get('kpa_col2') for d in candy]
        ret = displayCalc(listsSD)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQキャンディF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        """
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
        """



        #KPI質問7 F数
        sql = 'SELECT kpa_col1, kpa_col2 FROM t_report report '\
            'INNER JOIN t_kpi_answer kpa ON kpa.kpa_reportid = report.reportid '\
            'AND kpa.kpa_none = 0 AND kpa.kpa_delete = 0 '\
            'INNER JOIN t_kpi_question kpq ON kpq.kpq_kpiid = report.rp_kpiid '\
            'AND kpq.kpq_delete = 0 AND kpq.kpq_disporder = 7 '\
            'INNER JOIN t_kpi_row kpr ON kpr.kpr_kpiid = report.rp_kpiid '\
            'AND kpr.kpr_delete = 0 AND kpr.kpr_disporder = 1 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND kpq.kpqid = kpa.kpa_kpqid AND kpr.kprid = kpa.kpa_kprid '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s ORDER BY rp_date ASC'
        viscuit = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        listsHZ = [d.get('kpa_col1') for d in viscuit]
        ret = displayCalc(listsHZ)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQビスケットF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        listsSD = [d.get('kpa_col2') for d in viscuit]
        ret = displayCalc(listsSD)
        num = num + ret
        if row['clsp_chqid'] in chqs:
            #CHQビスケットF数
            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + ret

        """
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
        """

    #達成率の計算
    for k, v in chqs.items():
        if k in gChqs:
            gChqs[k]['all'] += v['all']
            gChqs[k]['num'] += v['num']
        else:
            gChqs[k] = v

    gTargetSum += targetSum
    gNum += num

    #月ループ　ここまで

#月を含めた全集計
if gTargetSum > 0:
    gRate = round(gNum / gTargetSum * 100, 2)

#chq別のカバレッジ、達成率
gChqs = list(gChqs.values())

for gchq in gChqs:
    if gchq['all'] > 0:
        gchq['rate'] = round(gchq['num'] / gchq['all'] * 100, 2)

#サマリーもJSONに含める
summary = {'all':gTargetSum, 'regi':gRegi, 'num':gNum, 'cavarege':gResult, 'rate':gRate}
response = {'summary': summary, 'detail': gChqs}
json_str = json.dumps(response, indent=2)

# json出力
h(json_str)
