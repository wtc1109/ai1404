#!/usr/bin/python
import MySQLdb
import time, os
print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="30" />
<title>AI software</title>
</head>
<body>
<h1>AI software</h1>"""

try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="AlgReturndb2")
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    cur = None
    print str(e)

if None != cur:
    _timeNow = time.time()
    a1 = cur.execute("select * from AiSoftwareVersion")
    if 0 != a1:
        print """<table><tr><td  width="200"> Name</td><td width="250">Version</td></tr>"""
        _devices = cur.fetchmany(a1)
        for dev in _devices:
            print "<tr><td>%s</td><td>%s</td></tr>" % (dev[0], dev[1])
        print "</table> "

print """</body> </html>"""



