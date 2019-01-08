#!/usr/bin/python
import MySQLdb
import time
print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="2" />
<title>New Device</title>
</head>
<body>
<h1>New Devices in 30 min</h1>
<table>
	<tr>
<td  width="200"> MAC</td><td width="150">cameraID</td><td width="200">time</td><td width="200">CPUINFO</td>
</tr>"""

try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="Producer")
    conn.autocommit(1)
    cur = conn.cursor()
except:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375")
    conn.autocommit(1)
    cur = conn.cursor()
    cur.execute("create database Producer")
    cur.execute("use Producer")
_timeNow = time.time()
a1 = cur.execute("select * from DeviceDB where time_int>%d"%int(_timeNow - 300*60))
if 0 != a1:
    _devices = cur.fetchmany(a1)
    _devs = sorted(_devices, key=lambda x:x[5], reverse=True)
    for dev in _devs:
        if dev[5] > (_timeNow-5*60):
            print "<tr><td>%s</td> <td>%s</td> <td bgcolor=red>%s</td> <td bgcolor=red>%s</td></tr>"%(dev[2], dev[3], dev[4], dev[0])
        else:
            print "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (dev[2], dev[3], dev[4], dev[0])
print """</table> </body> </html>"""



