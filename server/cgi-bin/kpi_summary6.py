#!/usr/bin/python3
# coding: utf-8
# 6 インプロ金額
import sys
import json
from dbAccessor import dbAccessor
from inputParser import inputParser
from my_function import h, e, int2
import xml.etree.ElementTree as ET
#import xmltodict

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


    #print(mon)

    #ターゲット数値取得
    chqs = obj.getTargetNum(6, mon['month'], mon['startdtstr'], mon['clientid'], mon['year'])

    #ターゲット店舗取得
    shops = obj.getTargetShop(6, mon['startdtstr'], mon['clientid'], mon['startdtYearmonth'], mon['enddtYearmonth'])

    #サマリー初期値
    targetSum = obj.getAllTargetNum(6, mon['month'], mon['clientid'], mon['year'])

    regi = 0
    num = 0
    result = 0
    rate = 0

    #ターゲット店舗毎に集計
    for row in shops:

        #対象外企業は除く
        if row['clsp_chqid'] not in chqs:
            continue

        #KPI質問6　該当店舗の範囲内の店頭情報回答すべて
        sql = 'SELECT reportid, rp_date, countid, ct_xml, cta_xml FROM t_report report '\
            'INNER JOIN t_count_ans cta ON cta.cta_reportid = report.reportid '\
            'AND cta.cta_delete = 0 '\
            'INNER JOIN t_count ct ON ct.countid = report.rp_countid '\
            'AND ct.ct_delete = 0 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s AND rp_count_none = 0'
        rows2 = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        #元となる商品辞書作成
        product_dict = {}

        for report in rows2:
            rp_date = report['rp_date']

            #レポート提出日付に対するターゲット商品
            items = obj.getTargetItem(mon['clientid'], rp_date)
            #扱いやすいように辞書型に加工
            item_dict = {}  #{'ｸﾛﾚｯﾂ': 5432,...
            for item in items:
                item_dict[item['ktp_product']] = item['price']

            #print(item_dict)
            
            # xml解析
            ct_root = ET.fromstring(report['ct_xml'])
            cta_root = ET.fromstring(report['cta_xml'])

            #質問から対象のQNOを取得
            qno = -1
            for i, product in enumerate(ct_root):

                #ターゲット商品でない場合は除く
                if (product.find('NAME').text not in item_dict):
                    continue

                product_name = product.find('NAME').text
                product_no = int(product.find('NO').text)
                product_dict[product_no] = {'PNAME':product_name, 'PRICE':item_dict[product_name]}

                if i == 0:
                    for question in product.findall('QUESTION'):
                        if question.find('TITLE').text == 'インプロ%R%Ball数':
                            qno = int(question.find('NO').text)

            #print(product_dict)

            #回答から対象のQNO回答を取得
            for i, product in enumerate(cta_root):
                result = 0
                pno = int(product.find('NO').text)

                if (pno not in product_dict):
                    continue
                
                #結果辞書にない場合は作成
                #if (pno not in result_dict):
                    #print('OK')
                    #result_dict[pno] = {'PNAME':product_dict[pno]['PNAME'], 'PNO':pno, 'RESULT':0}

                for answer in product.findall('QUESTION'):
                    if qno == int(answer.find('NO').text) and answer.find('ANS').text is not None:
                        if answer.find('ANS').text.isdecimal():
                            result = int(answer.find('ANS').text)
                            #print(pno)
                            #result_dict[pno]['RESULT'] = result_dict[pno]['RESULT'] + result
                            chqs[row['clsp_chqid']]['num'] = chqs[row['clsp_chqid']]['num'] + result * product_dict[pno]['PRICE']
        
    #shop毎ここまで

    #chqs カバレッジ、達成率の計算
    for k, v in chqs.items():
        if k in gChqs:
            gChqs[k]['num'] += v['num']
        else:
            gChqs[k] = v

    gTargetSum += targetSum
    gNum += num

    #月ループ　ここまで

#月を含めた全集計
gTargetSum = gTargetSum / len(posts.months)
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
