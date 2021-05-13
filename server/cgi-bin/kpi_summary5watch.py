#!/usr/bin/python3
# coding: utf-8
# 5 大陳数完了チェック
import cgi
import sys
import json
from dbAccessor import dbAccessor
from my_function import h, e
      
form = cgi.FieldStorage()
if 'keyid' not in form:
    json_str = json.dumps({'result': 'error', 'detail': 'keyid not found'})
    e(json_str)
    sys.exit()

keyid = int(form.getfirst('keyid', -1))

if keyid <= 0:
    json_str = json.dumps({'result': 'error', 'detail': 'keyid is invalid'})
    e(json_str)
    sys.exit()

# DBaccsess
obj = dbAccessor()
log = obj.checkSearchLog(keyid)

if len(log)==0:
    json_str = json.dumps({'result': 'execute', 'detail': ''})
    h(json_str)
else:
    json_log = log[0]['KPS_LOG']
    json_str = json.dumps({'result': 'done', 'detail': json_log})
    h(json_str)
