#!/usr/bin/env python
#Send message by dingding
# -*- coding:utf-8 -*-

#import python libs
import os,json,requests

def send_msg_by_dd():
    send_url = "https://oapi.dingtalk.com/robot/send?access_token=6062608ea58a3db097afc778bae48205ca8c94a69208a7bd7a757e4c6aef010b"
    header = {"Content-Type": "application/json;charset=utf-8"}
    send_data = {'msgtype':'markdown','markdown':{'title':None,'text':None},'at':{'isAtAll':'false'}}
    
    myalias = os.environ.get('NOTIFY_HOSTALIAS')
    if os.environ.get("NOTIFY_WHAT") == "SERVICE":
    	myserver = os.environ.get('NOTIFY_SERVICEDESC')
    	mystat = os.environ.get('NOTIFY_SERVICESTATE')
    	mytitle = "{0} {1} is {2}".format(myalias,myserver,mystat)
        mymessage = os.environ.get('NOTIFY_SERVICEOUTPUT')
    else:
    	mystat = os.environ.get("NOTIFY_HOSTSTATE")
    	mytitle =  "{0} is {1}".format(myalias,mystat)
        mymessage = os.environ.get('NOTIFY_HOSTOUTPUT')
    	
    mydate = os.environ.get('NOTIFY_SHORTDATETIME')
    
    myhost = os.environ.get('NOTIFY_HOSTADDRESS')
    
    #mymessage = os.environ.get('NOTIFY_SERVICEOUTPUT')
    
    try:
    	myoutput = os.environ.get('NOTIFY_LONGSERVICEOUTPUT')
    except:
    	myoutput = ""
    
    send_data['markdown']['title'] = mytitle
    mytext = u'''
**{0}**\n
Date:{1}\n
Host:{2}\n
Message:{3}
'''.format(mytitle,mydate,myhost,mymessage)
    send_data['markdown']['text'] = mytext
    response = requests.post(send_url,data = json.dumps(send_data),headers=header)
    print response.text

if __name__ == '__main__':
    send_msg_by_dd()
