#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://yjy.zabbix.letiku.net:18989/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# auth user and password
login_data = json.dumps(
{
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
   "user": "Admin",
   "password": "Yjy@yunwei123"
},
"id": 0
})
request = urllib2.Request(url,login_data)
for key in header:
   request.add_header(key,header[key])
# auth and get authid
try:
   result = urllib2.urlopen(request)
except URLError as e:
   print "Auth Failed, Please Check Your Name AndPassword:",e.code
else:
   response = json.loads(result.read())
   result.close()
auth_sessionid = response['result']

# 主机列表
data = json.dumps({
    "jsonrpc":"2.0",  
    "method":"host.get",  
    "params":{
        # "user": "Admin",
        # "password": "zabbix"  
        "output":["hostid","name"],  
        "filter":{"host":""}  
    },  
    "auth":auth_sessionid, # the auth id is what auth script returns, remeber it is string  
    "id":1,  
    }
)  

# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# auth and get authid
try:
   result = urllib2.urlopen(request)
except URLError as e:
   print "Auth Failed, Please Check Your Name AndPassword:",e.code
else:
   response = json.loads(result.read())
   result.close()
print response['result']
# print"Auth Successful. The Auth ID Is:",response[result]
# print "Number Of Hosts: ", len(response[result])  
# for host in response[result]:  
#    print "Host ID:",host['hostid'],"Host Name:",host['name']