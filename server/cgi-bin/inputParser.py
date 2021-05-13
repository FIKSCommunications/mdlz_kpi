#!/usr/bin/python3
# coding: utf-8
import cgi
import sys
import calendar
from datetime import datetime, date, timedelta
from my_function import h, e, get_last_date

class inputParser:

    def __init__(self):
        form = cgi.FieldStorage()

        """
        if 'startdt' not in form:
            e('not found startdt')
            sys.exit()
        if 'enddt' not in form:
            e('not found startdt')
            sys.exit()
        if 'clientid' not in form:
            e('not found clientid')
            sys.exit()
        """
        if 'startdt' not in form or 'enddt' not in form or 'clientid' not in form:
            #print('form')
            args = sys.argv

            if len(args) == 5:
                #print('args')
                self.startdt = args[1]
                self.enddt = args[2]
                self.clientid = args[3]
                self.keyid = args[4]
            else:
                #print('failed')
                self.startdt = '2021-01'
                self.enddt = '2021-01'
                self.clientid = 162
                self.keyid = -1
        else:
            #print('batch')
            self.startdt = form.getfirst('startdt', '2021-01')
            self.enddt = form.getfirst('enddt', '2021-01')
            self.clientid = form.getfirst('clientid', 162)
            self.keyid = -1

        """
        #単月対応
        self.startdtYearmonth = self.startdt.replace('-','')
        self.enddtYearmonth = self.enddt.replace('-','')

        #開始日終了日の取得
        self.today = datetime.today()
        self.todaystr = datetime.strftime(self.today, '%Y-%m-%d')
        self.todayYearmonth = datetime.strftime(self.today, '%Y-%m')
        self.yesterday = self.today - timedelta(days=1)
        self.yesterdaystr = datetime.strftime(self.yesterday, '%Y-%m-%d')
        self.yearmonth = datetime.strftime(self.yesterday, '%Y%m')

        #開始日
        self.startdtstr = self.startdt + '-01'

        #終了日
        #終了月が本日と同年月の場合は昨日とする
        if self.todayYearmonth == self.enddt:
            self.enddtstr = self.yesterdaystr
            enddts = self.enddtstr.split('-')
        else:
            enddts = self.enddt.split('-')
            self.enddtstr = get_last_date(int(enddts[0]), int(enddts[1]))

        #開始年、開始月
        startdts = self.startdt.split('-')
        self.year = int(startdts[0])
        self.month = int(startdts[1])
        """



        #複数月対応
        startdts = self.startdt.split('-')
        enddts = self.enddt.split('-')
        msu = (int(enddts[0]) - int(startdts[0])) * 12 + int(enddts[1]) - int(startdts[1]) + 1

        today = datetime.today()
        todayYearmonth = datetime.strftime(today, '%Y%m')
        yesterday = today - timedelta(days=1)
        yesterdaystr = datetime.strftime(yesterday, '%Y-%m-%d')

        self.months = []
        temp_y = int(startdts[0])
        temp_m = int(startdts[1])
        for i in range(msu):
            year = temp_y
            month = temp_m
            startdtYearmonth = str(temp_y) + str(temp_m).zfill(2)
            startdtstr = str(temp_y) + '-' + str(temp_m).zfill(2) + '-01'
            enddtYearmonth = startdtYearmonth

            #終了月が本日と同年月の場合は昨日とする
            if todayYearmonth == startdtYearmonth:
                enddtstr = str(yesterdaystr)
            else:
                enddtstr = str(get_last_date(temp_y, temp_m))

            thismonth = {
                'year':year, 
                'month':month, 
                'startdtYearmonth':startdtYearmonth,
                'startdtstr':startdtstr,
                'enddtYearmonth':enddtYearmonth,
                'enddtstr':enddtstr,
                'clientid':self.clientid,
            }
            self.months.append(thismonth)
            if temp_m < 12:
                temp_m = temp_m + 1
            else:
                temp_m = 1
                temp_y = temp_y + 1 
