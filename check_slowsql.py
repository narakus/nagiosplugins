#!/usr/bin/env python
# -*- conding -*-

import sys,MySQLdb

state_ok=0
state_warning=1
state_critical=2
state_unknown=3

def show_sql_list(host,username,passwd):
    db = MySQLdb.connect(host,username,passwd)
    cursor = db.cursor()
    try:
        cursor.execute('select id,user,command,time,info from information_schema.processlist')
        result = cursor.fetchall()
    except:
        print "Can't execute Sql in %s" %host
        sys.exit(state_unknown)
    finally:
        db.close()
    return result

def check_sql_list(d,w,c):
    clear_tuple = [ (sid,db,cmd,time,info) for sid,db,cmd,time,info in d if cmd != "Sleep" and int(time) > w ]
    #clear_tuple = [ (sid,db,cmd,time,info) for sid,db,cmd,time,info in d  if int(time) > w ]
    return clear_tuple

def alter(d,c):
    critical = False
    slowsql = []
    if not d:
        print "SLOW SQL OK - Total Slowsql = 0"
        sys.exit(state_ok)
    else:
        for sid,db,cmd,time,info in d:
            if int(time) > c:
                critical = True
            sqlstr = "runing %s time in %s database:%s" %(time,db,info)
            slowsql.append(sqlstr)
    output_str = ';'.join(slowsql)
    if critical:
        print  "SLOW SQL %s - Total Slowsql = %d, SLOWSQL:%s" %("CRITICAL",len(d),output_str)
        sys.exit(state_critical)
    print "SLOW SQL %s - Total Slowsql = %d, SLOWSQL:%s" %("WARNING",len(d),output_str)
    sys.exit(state_warning)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='check mysql slowsql')
    parser.add_argument('-i', action="store", dest="host",
                        required=False,help="mysql server host")
    parser.add_argument('-u', action="store", dest="username",
                        required=True,help="mysql username")
    parser.add_argument('-p', action="store", dest="passwd",
                        required=True,help="mysql password")
    parser.add_argument('-w', action="store", dest="warning",
                        type=int, required=False, help="nagios waring level")
    parser.add_argument('-c', action="store", dest="critical",
                        type=int, required=False, help="nagios critical level")
    args = parser.parse_args()
    if not args.host:
        args.host = "localhost"
    t = show_sql_list(args.host,args.username,args.passwd)
    m = check_sql_list(t,args.warning,args.critical)
    alter(m,args.critical)
