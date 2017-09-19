#!/usr/bin/python

import sys 
import urllib2
import base64
import json

def die(msg):
    print(msg)
    exit(1)

'''
echo "test" | ./send.py -h localhost -p 9999 -s "This is just command line test" -f "test@gmail.com" -t "test@gmail.com" -login test:test
'''

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
    elif i == '-s':
        skip = 'subject'
    elif i == '-f':
        skip = 'from'
    elif i == '-t':
        skip = 'to'
    elif i == '-a':
        skip = 'attach'
    elif i == '-login':
        skip = 'login'

if 'host' not in data:
    die("host is missing use -h option")

if 'port' not in data:
    die("port is missing use -p option")

if 'subject' not in data:
    die("subject is missing use -s option")

if 'from' not in data:
    die("from is missing use -f option")

if 'to' not in data:
    die("to is missing use -t option")

data['content'] = raw_input("Enter content of the email \n")

built = {
	"from": data['from'],
	"recieve": {
		"to" : [
			{
				"email": data['to'],
				"name": "John Doe"
			}
		]
	}, 
	"subject": data['subject'], 
	"body": data['content'] if data['content'] != '' else '.', 
}


handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
print "http://%s:%s" % (data['host'], data['port'])
request = urllib2.Request("http://%s:%s/send" % (data['host'], data['port']), data=json.dumps(built))

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
