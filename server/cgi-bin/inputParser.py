#!C:\Users\m-neishi\AppData\Local\Programs\Python\Python39\python.exe
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
        self.startdt = form.getfirst('startdt', '2021-01')
        self.enddt = form.getfirst('enddt', '2021-01')
        self.clientid = form.getfirst('clientid', 162)

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
        else:
            enddts = self.enddt.split('-')
            self.enddtstr = get_last_date(int(enddts[0]), int(enddts[1]))

        #開始年、開始月
        startdts = self.startdt.split('-')
        self.year = int(startdts[0])
        self.month = int(startdts[1])
    
