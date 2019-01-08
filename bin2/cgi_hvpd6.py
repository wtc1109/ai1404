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
    conn = MySQLdb.connect(host="localhost", user="bluecardsoft", passwd="#$%_BC13439677375", db="AlgReturndb2")
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

        if 0 == cur.execute("select * from aiouttable where cameraID='%s' and cmosID=%d" %(_hvpd[0], _hvpd[1])):
            continue
        _aiout1 = cur.fetchone()
        if 0 == cur.execute("select * from reoutfiltertable where cameraID='%s' and cmosID=%d" % (_hvpd[0], _hvpd[1])):
            continue
        _reout1 = cur.fetchone()
        _spaces = 3
        if None != _aiout1 and None != _aiout1[4]:
            _spaces = _aiout1[4]
            _aiout = "%d:%d"%(_aiout1[4],_aiout1[5])
            for i in range(1,_aiout1[4]):
                _aiout +=",%d"%_aiout1[5+i]
        else:
            _aiout = 'None'

        _reout = []
        for i in range(3):
            _reout.append('NULL')
        if None != _reout1:
            for i in range(_spaces):
                if 1 == _aiout1[5+i] and None != _reout1[4+5*i]:
                    _reout[i]=_reout1[4+5*i]
                    #for cc in _reout1[3+4*i]:
                    #    print '%02X'%ord(cc)
        for i in range(_spaces,3):
            _reout[i] = ' '

        _sn1_a = "<a href='http://%s/setting.html' target='_blank'>%s</a>" % (_hvpd[4], _hvpd[0])
        _cmos1_a = "<a href='http://%s/images/' target='_blank'>cmos%d</a>"\
                   % (_hvpd[4], _hvpd[1])
        _lines.append((_hvpd[4], _sn1_a,_cmos1_a,_aiout, _reout))

    _pos = 0
    for _line in _lines:

        print """
            <tr>
<td><img src="http://%s/images/orig0.jpg" width="1153", hight="648" /></td>
<td><p>%s %s</p><p>%s</p>
<p>%s</p><p>%s</p><p>%s</p></td></tr>
            """%(_line[0],_line[1],_line[2],_line[3], _line[4][0], _line[4][1], _line[4][2])

    print "</table>"
else:
    print """connect DB fault"""

print "</body> </html>"