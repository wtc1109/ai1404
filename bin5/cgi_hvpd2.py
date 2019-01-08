import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<title>Double Cameras Hvpds</title>
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
    b1 = cur.execute("select * from equipment2cameraidmem where cameraID2 is not null")
    print "Get %d hvpds"%b1
    print """
    <table><tr>
    <td width="220"></td>
    <td width="220"></td>
    <td></td>
    <td width="220"></td>
    <td width="220"></td>
    <td></td></tr>
    """
    _hvpds = cur.fetchmany(b1)
    _lines = []
    for _hvpd in _hvpds:
        cur.execute("select * from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d" %(_hvpd[2], _hvpd[3]))
        _online1 = cur.fetchone()
        cur.execute("select * from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d" %(_hvpd[4], _hvpd[5]))
        _online2 = cur.fetchone()
        if None == _online1 or None == _online2:
            continue
        cur.execute("select * from aiouttable where cameraID='%s' and cmosID=%d" %(_hvpd[2], _hvpd[3]))
        _aiout1 = cur.fetchone()
        cur.execute("select * from aiouttable where cameraID='%s' and cmosID=%d" %(_hvpd[4], _hvpd[5]))
        _aiout2 = cur.fetchone()

        if None != _aiout1:
            _aiout = "%d:%d"%(_aiout1[4],_aiout1[5])
            for i in range(1,_aiout1[4]):
                _aiout +=",%d"%_aiout1[5+i]
        else:
            _aiout = 'None'
        if None != _aiout2:
            _aiout += " | %d:%d" % (_aiout2[4], _aiout2[5])
            for i in range(1, _aiout2[4]):
                _aiout += ",%d"%_aiout2[5+i]
        else:
            _aiout += ' | None'
        if None != _hvpd[6]:
            _col_str = _hvpd[6].split(",")
            _col2 = []
            _col_int = 0

            for i in range(3):
                _col_spl = _col_str[i].split(":")
                _col2.append(_col_spl)
                if _col_int < int(_col_spl[1]):
                    _col_int=int(_col_spl[1])
            if 0 == _col_int:
                _color = "#000000"
            else:
                _color = "#"
                _mul = 255.0/_col_int
                for i in range(3):
                    _color += "%02X"%(int(_mul*int(_col2[i][1])))
        else:
            _color = '#000000'




        _sn1_a = "<a href='http://%s/setting.html' target='_blank'>%s</a>" % (_online1[4], _online1[0])
        _cmos1_a = "<a href='http://%s/images/' target='_blank'>cmos%d</a>" % (_online1[4], _online1[1])
        _sn2_a = "<a href='http://%s/setting.html' target='_blank'>%s</a>" % (_online2[4], _online2[0])
        _cmos2_a = "<a href='http://%s/images/' target='_blank'>cmos%d</a>" % (_online2[4], _online2[1])
        _lines.append((_online1[4], _online2[4],_sn1_a,_cmos1_a,_sn2_a,_cmos2_a,_aiout,_color))

    _pos = 0
    for _line in _lines:
        if 0 == _pos:
            print """
            <tr><td><img src="http://%s/images/ai0.jpg" width="200", hight="200" /></td>
<td><img src="http://%s/images/ai0.jpg" width="200", hight="200" /></td>
<td><p><font size="5" color="%s">%s %s</font></p>
<p><font size="5" color="%s">%s %s</font></p>
<p><font size="5" color="%s">%s</font></p></td>
            """%(_line[0],_line[1],_line[7],_line[2],_line[3],_line[7],_line[4],_line[5],_line[7],_line[6])
            _pos = 1
        else:
            print """
            <td><img src="http://%s/images/ai0.jpg" width="200", hight="200" /></td>
<td><img src="http://%s/images/ai0.jpg" width="200", hight="200" /></td>
<td><p><font size="5" color="%s">%s %s</font></p>
<p><font size="5" color="%s">%s %s</font></p>
<p><font size="5" color="%s">%s</font></p></td></tr>
            """%(_line[0],_line[1],_line[7],_line[2],_line[3],_line[7],_line[4],_line[5],_line[7],_line[6])
            _pos = 0
    if 0 != _pos:
        print "<td></td><td></td><td></td></tr>"
    print "</table>"
else:
    print """connect DB fault"""

print "</body> </html>"