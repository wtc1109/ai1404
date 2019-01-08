import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>GBK HVPD</title>
</head>
<body>
"""
try:
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="hvpd3db2")
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    cur = None
    print str(e)

if None != cur:
    a1 = cur.execute("select * from onlinehvpdstatustablemem")
    print "Get %d hvpds online"%a1
    print """
    <table><tr>
    <td width="1155"></td>
    <td></td></tr>
    """
    _hvpds = cur.fetchmany(a1)
    _lines = []
    for _hvpd in _hvpds:

        if 0 == cur.execute("select bays from aiouttable_camera where cameraID='%s' and cmosID=%d" %(_hvpd[0], _hvpd[1])):
            continue
        _bays, = cur.fetchone()
        _aiout1 = []

        _reout2 = []
        _err = 0
        for i in range(_bays):
            if 0 == cur.execute("select State from aiouttable_bay where cameraID='%s' and cmosID=%d and bay=%d" % (_hvpd[0], _hvpd[1],i+1)):
                _err = 1
                break
            _state, = cur.fetchone()
            _aiout1.append(_state)
            _st = ''
            if 1 == _state:
                if 0 != cur.execute("select PlateNumber from reoutfiltertable where cameraID='%s' and cmosID=%d and bay=%d" % (_hvpd[0], _hvpd[1], i+1)):
                    _st, = cur.fetchone()
                    if None == _st:
                        _st = ''

            _reout2.append(_st)
        if 0 != _err:
            continue
        _aiout = "%d:%d" %(_bays,_aiout1[0])
        for i in range(1, _bays):
            _aiout += ',%d'%_aiout1[i]

        _sn1_a = "<a href='http://%s/setting.html' target='_blank'>%s</a>" % (_hvpd[4], _hvpd[0])
        _cmos1_a = "<a href='http://%s/images/' target='_blank'>cmos%d</a>" \
                   % (_hvpd[4], _hvpd[1])
        print """<tr><td><img src="http://%s/images/orig0.jpg" width="1153", hight="648" /></td>
        <td><p>%s %s</p><p>%s</p>""" % (_hvpd[4], _sn1_a, _cmos1_a, _aiout)

        _reout = []
        for i in range(_bays):
            _reout.append('NULL')
            if '' == _reout2[i]:
                print "<p>NULL</p>"
            else:
                print "<p>%s</p>"%( _reout2[i])

        print "</td></tr>"

    print "</table>"
else:
    print """connect DB fault"""

print "</body> </html>"