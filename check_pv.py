#!/usr/bin/env python

import json
import requests
from datetime import date

state_ok=0
state_warning=1
state_critical=2
state_unknown=3

default_time = date.today().strftime('%Y%m%d')

def check_pv(host,name,mydate=default_time):
    request_str = host + '?domain=' + name
    response = requests.get(request_str)
    return response.json()

def myprint(name,jsondata):
    states = jsondata['state']
    mystr = ''
    for s,v in states.items():
        mystr += 'status_of_' + s.encode() + ':' + str(v) +';'
    result = '{} pv:{} uv:{} {}|pv={};;;;uv={};;;;'.format(name,jsondata['pv'],jsondata['uv'],mystr,
                                                         jsondata['pv'],jsondata['uv'] )
    for state,value in states.items():
       result = result + 'status_of_' + state.encode() + '=' + str(value) + ';;;;'
    print result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='check websit pv uv state')
    parser.add_argument('-i', action="store", dest="host",
                       required=True,help="mysql server host")
    parser.add_argument('-n', action="store", dest="domainname",
                        required=True,help="domain name")
    parser.add_argument('-d', action="store", dest="date",
                        required=False,help="search date,default today")
    args = parser.parse_args()

    mydata = check_pv(args.host,args.domainname)
    #output = '{} pv:{} uv:{} |pv={};;;;uv={};;;;state_of_200={};;;;state_of_401={};;;;state_of_404={};;;;state_of_412={};;;;'.format(args.domainname,mydata['pv'],mydata['uv'],mydata['pv'],mydata['uv'],mydata['state']['200'],mydata['state']['401'],mydata['state']['404'],mydata['state']['412'])
    #print output
    myprint(args.domainname,mydata)
