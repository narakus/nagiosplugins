#!/usr/bin/env python

import sys
import requests

state_ok=0
state_warning=1
state_critical=2
state_unknown=3

def check_els_status(url):
    try:
        response = requests.get(url)
    except Exception as e:
       print e.message
       sys.exit(state_unknown)
    result = response.json()
    status = result['status']
    outline = '{} status is {}, active_primary_shards:{}, number_of_data_nodes:{}, number_of_nodes:{}'.format(
               result['cluster_name'],result['status'],result['active_primary_shards'],
               result['number_of_data_nodes'],result['number_of_nodes'])
    print outline
    if status != 'red':
        sys.exit(state_ok)
    else:
        sys.exit(state_critical)
         
if __name__ == '__main__':
    url = sys.argv[1]
    check_els_status(url)
