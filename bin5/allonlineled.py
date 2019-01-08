#!/usr/bin/python
import MySQLdb
import time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="30" />
<title>LED displayer</title>
</head>
<body>
<h1>LED displayer</h1>
"""


try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="hvpd3db2")
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    cur = None
    print str(e)

if None != cur:

    _timeNow = time.time()
    a1 = cur.execute("select * from LedDisplayerUdpInfo")
    if 0 != a1:
        print "found %d LED displayers online"%a1
        print """<table><tr>
        <td  width="150"> SN</td><td width="70">width</td><td width="70">height</td><td width="180">Version</td><td width="200">Connect time</td>
        </tr>"""
        _devices = cur.fetchmany(a1)
        for dev in _devices:
            print "<tr><td>%s</td> <td>%d</td> <td>%d</td><td>%s</td> <td>%s</td></tr>" % (dev[1], dev[2], dev[3], dev[11],dev[19])
        print "</table> "
    else:
        print "found 0 LED displayer"
print """</body> </html>"""



