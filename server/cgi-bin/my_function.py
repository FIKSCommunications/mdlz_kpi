#!/usr/bin/python3
# coding: utf-8
import calendar
from datetime import datetime, date, timedelta

#header出力用
def h(contents):
    print('Status: 200 OK')
    print('Content-Type: text/html\nAccess-Control-Allow-Origin: *\n')
    print('\n\n')
    print(contents)
    print('\n')

def e(contents):
    print('Status: 400 BAD REQUEST')
    print('Content-Type: text/html\nAccess-Control-Allow-Origin: *\n')
    print('\n\n')
    print(contents)
    print('\n')

#月の最終日を求める
def get_last_date(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])

#数値変換
def int2(num):
    if num.isdecimal():
        return int(num)
    else:
        # 2.などドットを含む場合はドット以降を切り捨て
        if num.find('.') > 0 and num[0:num.find('.')].isdecimal: 
            return int(num[0:num.find('.')])
        else:
            return 0





