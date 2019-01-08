#!/usr/bin/python
import MySQLdb
import time
print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="30" />
<title>HVPDS</title>
</head>
<body>
<h1>All Online HVPDS</h1>
"""

try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="AlgReturndb2")
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    cur = None
    print str(e)

if None != cur:

    _timeNow = time.time()
    a1 = cur.execute("select * from onlinehvpdstatustablemem")
    if 0 != a1:
        print "found %d HVPDS online"%a1
        print """<table><tr>
        <td  width="150"> SN</td><td width="50">cmos</td><td width="100">Images</td><td width="200">Connect time</td>
        </tr>"""
        _devices = cur.fetchmany(a1)
        for dev in _devices:
            _alink = "<a href='http://%s/'>Picture</a>" %dev[4]
            print "<tr><td>%s</td> <td>%d</td> <td>%s</td> <td>%s</td></tr>" % (dev[0], dev[1], _alink, dev[9])
        print "</table> "
    else:
        print "found 0 HVPD"
print """</body> </html>"""



