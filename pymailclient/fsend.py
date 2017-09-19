#!/usr/bin/python

'''
python fsend.py -h localhost -p 9999 -f test.json -login test:test
'''

import sys 
import urllib2
import base64
import json
import os

def die(msg):
    print(msg)
    exit(1)


skip=None
data = {}
for i in sys.argv[1:]:
    if skip is not None:
        data[skip] = i 
        skip = None;
        continue 
    
    if i == '-h':
        skip = 'host'
    elif i == '-p':
        skip = 'port'
    elif i == '-login':
        skip = 'login'
    elif i == '-f':
        skip = 'file'

if 'host' not in data:
    die("host is missing use -h option")

if 'port' not in data:
    die("port is missing use -p option")

if 'file' not in data:
    die("file is missing use -f option")


if not os.path.isfile(data['file']):
    die("File not found")

content = None
with open(data['file']) as f:
    content = f.read()

if content is None:
    die("File is empty")

handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
print "http://%s:%s" % (data['host'], data['port'])
request = urllib2.Request("http://%s:%s/send" % (data['host'], data['port']), data=content)

request.add_header("Content-Type",'application/json')

if 'login' in data:
    request.add_header("Authorization", "Basic %s" % base64.encodestring(data['login']).replace('\n', ''))

request.get_method = lambda: "POST"

try:
    connection = opener.open(request)
except urllib2.HTTPError,e:
    connection = e

# check. Substitute with appropriate HTTP code.
if connection.code == 200:
    data = connection.read()
    print data
    exit(0)
else:
    print "Error"
    print connection.code
    exit(1)
