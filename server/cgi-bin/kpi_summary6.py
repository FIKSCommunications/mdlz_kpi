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
    targetSum = 55697537  #ここはCSVから取得
    regi = 0
    num = 0
    result = 0
    rate = 0


    #ターゲット店舗毎に集計
    for row in shops:

        #KPI質問1　回答:レジ台数
        sql = 'SELECT countid, ct_xml, cta_xml FROM t_report report '\
            'INNER JOIN t_count_ans cta ON cta.cta_reportid = report.reportid '\
            'AND cta.cta_delete = 0 '\
            'INNER JOIN t_count ct ON ct.countid = report.rp_countid '\
            'AND ct.ct_delete = 0 '\
            'WHERE rp_delete = 0 AND rp_done = 1 '\
            'AND rp_clientid = %s AND rp_shopid = %s AND rp_date <= %s '\
            'AND rp_date >= %s ORDER BY rp_date DESC LIMIT 1'
        rows2 = obj.execQuery(sql, [mon['clientid'], row['kts_shopid'], mon['enddtstr'], mon['startdtstr']])

        if len(rows2) > 0:
            # xml解析
            '''
            print(rows2[0]['countid'])
            ct_dict = xmltodict.parse(rows2[0]['ct_xml'],force_list=('PRODUCT'))
            cta_dict = xmltodict.parse(rows2[0]['cta_xml'],force_list=('PRODUCT'))
            for countans in cta_dict['CTA_XML']['PRODUCT']:
                for qans in countans['QUESTION']:
                    if qans['NO'] == '5':
                        print('www')
                        print(qans['ANS'])
                        break

            result = {}
            for product in ct_dict['CT_XML']['PRODUCT']:
                print(product['NAME'])
                print(product['NO'])
            '''

            ct_root = ET.fromstring(rows2[0]['ct_xml'])
            cta_root = ET.fromstring(rows2[0]['cta_xml'])

            #元となる商品辞書作成
            product_dict = {}
            qno = -1
            for i, product in enumerate(ct_root):
                product_name = product.find('NAME').text
                product_no = int(product.find('NO').text)
                product_dict[product_no] = {'PNAME':product_name, 'PNO':product_no, 'RESULT':0}

                if i == 0:
                    for question in product.findall('QUESTION'):
                        if question.find('TITLE').text == 'インプロ%R%Ball数':
                            qno = int(question.find('NO').text)

            #print(qno)

            for i, product in enumerate(cta_root):
                result = 0
                pno = int(product.find('NO').text)
                #print(pno)
                for answer in product.findall('QUESTION'):
                    if qno == int(answer.find('NO').text) and answer.find('ANS').text is not None:
                        if answer.find('ANS').text.isdecimal():
                            print('www')
                            result = int(answer.find('ANS').text)
                            print(pno)
                            product_dict[pno]['RESULT'] = product_dict[pno]['RESULT'] + result

            #print(product_dict)
            sys.exit()




            dict_q = {}
            for child in ct_root:
                pname = child.find('NAME').text
                pno = child.find('NO').text
                dict_q[pname] = pno

                questions = child.findall('.//TITLE')
                questionNos = child.findall('.//NO')
                for i, question in enumerate(questions):
                    if question.text == 'インプロ%R%Ball数':
                        print(questionNos[i+1].text)
                        break
            
            for child in cta_root:
                products = child.findall('./QUESTION')



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

    gTargetSum += targetSum
    gRegi += regi
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
