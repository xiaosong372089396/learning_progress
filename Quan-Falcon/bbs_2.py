#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'xiaosong'

import sys
import urllib2
import base64
import json
import time
import socket
import commands

def get_endPoint():
    redis_hostname = socket.gethostname()
    ip_list = commands.getoutput(''' ip a|grep 'inet ' |grep -v "127.0."  |awk '{print $2}' |awk -F"/" '{print $1}' ''').split("\n")
    for ip in ip_list:
        ip = ip.strip()
        if ip.startswith("192."):
            return "%s-%s"%(redis_hostname,ip)
        elif ip.startswith("172."):
            return "%s-%s"%(redis_hostname,ip)
        elif ip.startswith("10."):
            return "%s-%s"%(redis_hostname,ip)


step = 60
ip = get_endPoint()
ts = int(time.time())
bbs = 'bbsapp'
keys_get = ['/bbs/user/login.json', '/bbs/bbs/info.json']
key_post = ('bbs_user_login', 'bbs_user_heartbeat', 'bbs_board_create', 'bbs_board_update', 'bbs_create', 'bbs_list_by_editor', \
				'bbs_comment_create', 'bbs_pic_save_thumb', 'bbs_pic_destroy', 'bbs_stat_board_unread', 'bbs_stat_bbs_comment_count')

rates = ('ack', 'deliver', 'deliver_get', 'publish')

# http://testcloudb.quanshi.com
for getUrl in keys_get:
	request = urllib2.Request("https://oncloud.quanshi.com//%s/%s" % (bbs,str(getUrl)))
	result = urllib2.urlopen(request)
	data = result.getcode()
	tag = ''
	# tag = sys.argv[1].replace('_',',').replace('.','=')
	p = []
    #	for queue in data:
	msg_total = 0

	q = {}
	q["endpoint"] = ip
	q['timestamp'] = ts
	q['step'] = step
	q['counterType'] = "GAUGE"
	q['metric'] = 'bbsapp.%s' % getUrl
	q['tags'] = 'name=%s,%s' %  (bbs, getUrl)
	q['value'] = data
	p.append(q)
	print json.dumps(p, indent=4)

method = "POST"
handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
url = 'http://127.0.0.1:1988/v1/push'
request = urllib2.Request(url, data=json.dumps(p) )
request.add_header("Content-Type",'application/json')
request.get_method = lambda: method
try:
    connection = opener.open(request)
except urllib2.HTTPError,e:
    connection = e
if connection.code == 200:
    print connection.read()
else:
    print '{"err":1,"msg":"%s"}' % connection
