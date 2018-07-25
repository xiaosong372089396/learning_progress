#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys
import re
import json
import requests
import time
import urllib2
import base64
from socket import *

def checkPing(host):
    result=os.popen("ping -i 0.1 -c 10 %s | tail -n 2 | tail -n 1 | awk -F\/ '{print $5}'"%host).read()
    try:
        result=int(float(result.replace("\n",'')))
    except:
        result = -1
    return result


def uploadToAgent(p):
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = "http://127.0.0.1:1988/v1/push"
    request = urllib2.Request(url, data=json.dumps(p))
    request.add_header('Content-Type','application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e
    if connection.code == 200:
        print connection.read()
    else:
        print '{"err":1,"msg":"%s"}' % connection
print "开始 "


def zuzhuangData(tags = '', value = ''):
    endpoint = "172.16.10.99"
    metric = "userdefine"
    key = "icmp"
    timestamp = int(time.time())
    step = 60
    vtype = "GAUGE"

    i = {
            'Metric' :'%s.%s'%(metric,key),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': step,
            'value': value,
            'CounterType': vtype,
            'TAGS': tags
            }
    return i

p = []
with open("./icmp.txt") as f:
    for line in f:
        results = re.findall("(\S+)",line)
        print results
        host = results[0]
    description = results[1]
        tags = "project=ops,"
        tags += "host=%s,description=%s"%(host,description)
        value = checkPing(host)
        p.append(zuzhuangData(tags,value))

print json.dumps(p, sort_keys=True,indent = 4)

uploadToAgent(p)