import os,MySQLdb,time

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=gbk" http-equiv="content-type">
<title>VLPR cur</title>
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
    _err_b1 = 0
    _err_b2 = 0
    _err_b3 = 0
    _b1 = cur.execute("select cameraID,Plate1Number from reouttable where length(Plate1Number)>3")
    if 0 != _b1:
        _plate1s1 = cur.fetchall()
        cur.execute("select cameraID,Plate1Number from reoutfiltertable where length(Plate1Number)>3")
        staisitc_plate1s1 = cur.fetchall()
        _plate1s = {}
        staisitc_plate1s = {}
        for i in range(_b1):
            _plate1s.update({"%s"%_plate1s1[i][0]:"%s"%_plate1s1[i][1]})
            staisitc_plate1s.update({"%s"%staisitc_plate1s1[i][0]:"%s"%staisitc_plate1s1[i][1]})
        for _key in _plate1s:
            if not _key in staisitc_plate1s:
                _err_b1 += 1
                continue
            if _plate1s[_key] != staisitc_plate1s[_key]:
                _err_b1 += 1

    _b2 = cur.execute("select cameraID,Plate2Number from reouttable where length(Plate2Number)>3")
    if 0 != _b2:
        _plate1s1 = cur.fetchall()
        cur.execute("select cameraID,Plate2Number from reoutfiltertable where length(Plate2Number)>3")
        staisitc_plate1s1 = cur.fetchall()
        _plate1s = {}
        staisitc_plate1s = {}
        for i in range(_b2):
            _plate1s.update({"%s" % _plate1s1[i][0]: "%s" % _plate1s1[i][1]})
            staisitc_plate1s.update({"%s" % staisitc_plate1s1[i][0]: "%s" % staisitc_plate1s1[i][1]})
        for _key in _plate1s:
            if not _key in staisitc_plate1s:
                _err_b2 += 1
                continue
            if _plate1s[_key] != staisitc_plate1s[_key]:
                _err_b2 += 1

    _b3 = cur.execute("select cameraID,Plate3Number from reouttable where length(Plate3Number)>3")
    if 0 != _b3:
        _plate1s1 = cur.fetchall()
        cur.execute("select cameraID,Plate3Number from reoutfiltertable where length(Plate3Number)>3")
        staisitc_plate1s1 = cur.fetchall()
        _plate1s = {}
        staisitc_plate1s = {}
        for i in range(_b3):
            _plate1s.update({"%s" % _plate1s1[i][0]: "%s" % _plate1s1[i][1]})
            staisitc_plate1s.update({"%s" % staisitc_plate1s1[i][0]: "%s" % staisitc_plate1s1[i][1]})
        for _key in _plate1s:
            if not _key in staisitc_plate1s:
                _err_b3 += 1
                continue
            if _plate1s[_key] != staisitc_plate1s[_key]:
                _err_b3 += 1

    #print "Get %d plates"%(b1+_b2+ _b3)
    cur.execute("select count(parking1State) from aiouttable where plate1posLTx!=0 and plate1posLTy!=0 and plate1posRBx!=0 and plate1posRBy!=0")
    _c1, = cur.fetchone()
    cur.execute(
        "select count(parking2State) from aiouttable where plate3posLTx!=0 and plate3posLTy!=0 and plate3posRBx!=0 and plate3posRBy!=0")
    _c2, = cur.fetchone()
    cur.execute(
        "select count(parking3State) from aiouttable where plate5posLTx!=0 and plate5posLTy!=0 and plate5posRBx!=0 and plate5posRBy!=0")
    _c3, = cur.fetchone()


    cur.execute("select count(Plate1Number) from reoutfiltertable where length(Plate1Number)>5")
    _d1, = cur.fetchone()
    cur.execute("select count(Plate2Number) from reoutfiltertable where length(Plate2Number)>5")
    _d2, = cur.fetchone()
    cur.execute("select count(Plate3Number) from reoutfiltertable where length(Plate3Number)>5")
    _d3, = cur.fetchone()
    print """
    <table><tr>
    <td width="205"></td>
    <td width="205"></td>
    <td width="205"></td></tr>
    """

    print "<tr><td></td><td>plate all:</td><td>%d</td></tr>"%(_b1+_b2+ _b3)
    print "<tr><td></td><td>plate error:</td><td>%d</td></tr>"%(_err_b1 + _err_b2 + _err_b3)
    if 0 != (_b1+_b2+ _b3):
        print "<tr><td></td><td>OK persent:</td><td>%f</td></tr>" % (1.0-
        1.0 * (_err_b1 + _err_b2 + _err_b3) / (_b1 + _b2 + _b3))
        print "<tr><td></td><td>Error persent:</td><td>%f</td></tr>"%(1.0*(_err_b1 + _err_b2 + _err_b3)/(_b1+_b2+ _b3))
    print "<tr><td></td></tr><tr><td></td></tr>"
    print "<tr><td></td><td>all Cars:</td><td>%d</td></tr>" % (_c1 + _c2 + _c3)
    print "<tr><td></td><td>all vlpr result:</td><td>%d</td></tr>" % (_d1 + _d2 + _d3)
    _percent = 1.0*(_d1 + _d2 + _d3)/(_c1 + _c2 + _c3)
    print "<tr><td></td><td>vlpr percent:</td><td>%f</td></tr>" % _percent
    print "<tr><td></td><td>nolpr percent:</td><td>%f</td></tr>" % (1.0 - _percent)
    print "</table>"
else:
    print """connect DB fault"""

print "</body> </html>"