import os,sqlite3,time
import cgi, cgitb, shutil,wtclib

def get_sqlite_cur(DBname):
    try:
        conn = sqlite3.connect(DBname)
        conn.isolation_level = None
        cur = conn.cursor()
    except:
        conn = sqlite3.connect()
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("create database %s"%DBname)
        cur.execute("use %s"%DBname)
    return cur, conn

def str_is_ip(str1):
    _list1 = str1.split('.')
    if 4 != len(_list1):
        return -1
    try:
        for i in range(4):
            i1 = int(_list1[i])
            if i1 > 255 or i1 < 0:
                return -2
        return 0
    except Exception,e:
        print e
        return -3


print "Content-type:text/html\n\n"
print """<html >
<head>
<meta content="text/html;charset=utf-8" http-equiv="content-type">
<title>Settings</title>
</head>
 <body>
 <form method="post" action="/cgi-bin/adv.sh" name="adv_set">
 <h2>Advance Settings</h2>
 <ul>
  <li><h3>Who am I</h3></li>
"""
form = cgi.FieldStorage()
_dict1 = {}
for key in form.keys():
    _dict1.update({key:form[key].value})
try:
    sqlite_cur, hvpd_conn = get_sqlite_cur("adv_set.db")
    sqlite_cur.execute("select val from setting where name='Co_server'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('Co_server','0')")

    sqlite_cur.execute("select val from setting where name='ai_ip'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('ai_ip','0')")

    sqlite_cur.execute("select val from setting where name='ai_f'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('ai_f','0')")

    sqlite_cur.execute("select val from setting where name='vlpr_f'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('vlpr_f','0')")

    sqlite_cur.execute("select val from setting where name='h264_f'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('h264_f','0')")

    sqlite_cur.execute("select val from setting where name='ctl_ip'")
    _a1 = sqlite_cur.fetchone()
    if None == _a1:
        sqlite_cur.execute("insert into setting (name,val)values('ctl_ip','0')")

    if "FacDefaultA" in _dict1:
        _Co_server = '0'
        _ai_ip = 0
        _ai_f = '0'
        _vlpr_f = '0'
        _h264_f = '0'
        _ctl_ip = 0

    else:
        _Co_server = '0'
        if "Co_server" in _dict1:
            _Co_server = _dict1["Co_server"]
        else:
            sqlite_cur.execute("select val from setting where name='Co_server'")
            _a1 = sqlite_cur.fetchone()
            if None != _a1:
                if '1' == _a1[0]:
                    _Co_server = '1'

        _ai_ip = 0
        if "ai_ip" in _dict1:
            if 0 == str_is_ip(_dict1['ai_ip']):
                _ai_ip = _dict1['ai_ip']
        else:
            sqlite_cur.execute("select val from setting where name='ai_ip'")
            _ip = sqlite_cur.fetchone()
            if _ip != None:
                if 0 == str_is_ip(_ip[0]):
                    _ai_ip = _ip[0]

        _ai_f = '0'
        if "ai_f" in _dict1:
            _ai_f = _dict1['ai_f']
        else:
            sqlite_cur.execute("select val from setting where name='ai_f'")
            _a1 = sqlite_cur.fetchone()
            if None != _a1:
                if '1' == _a1[0]:
                    _ai_f = '1'

        _vlpr_f = '0'
        if "vlpr_f" in _dict1:
            _vlpr_f = _dict1['vlpr_f']
        else:
            sqlite_cur.execute("select val from setting where name='vlpr_f'")
            _a1 = sqlite_cur.fetchone()
            if None != _a1:
                if '1' == _a1[0]:
                    _vlpr_f = '1'

        _h264_f = '0'
        if "h264_f" in _dict1:
            _h264_f = _dict1['h264_f']
        else:
            sqlite_cur.execute("select val from setting where name='h264_f'")
            _a1 = sqlite_cur.fetchone()
            if None != _a1:
                if '1' == _a1[0]:
                    _h264_f = '1'


        _ctl_ip = 0
        if "ctl_ip" in _dict1:
            if 0 == str_is_ip(_dict1['ctl_ip']):
                _ctl_ip = _dict1['ctl_ip']
        else:
            sqlite_cur.execute("select val from setting where name='ctl_ip'")
            _ip = sqlite_cur.fetchone()
            if None != _ip:
                if 0 == str_is_ip(_ip[0]):
                    _ctl_ip = _ip[0]

    fp = open('../../../hvpd/prog/bin/sh.sh','w')
    fp.write("""#!/bin/sh
cd /home/bluecard/hvpd/prog/bin
chmod 0777 *
killall amqp_consumer
killall amqp_bind
killall rtsp_client
killall python
rm *.mp4
python ai_init.pyc &
sleep 1
python createdb.pyc 
chmod 666 /tmp/softdog.db
sleep 3\n""")

    if 0 != _ai_ip and '0' != _Co_server:
        sqlite_cur.execute("update setting set val='1' where name='Co_server'")
        sqlite_cur.execute("update setting set val='%s' where name='ai_ip'"%(_ai_ip))
        _localt = time.localtime()
        _dst = 'conf.%d%02d%02d.%02d%02d%02d'%(_localt.tm_year, _localt.tm_mon, _localt.tm_mday,
                                               _localt.tm_hour, _localt.tm_min, _localt.tm_sec)
        shutil.copy('../../../hvpd/prog/conf/conf.conf','../../../hvpd/prog/conf/%s'%_dst)
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf','ucmq',{'server_addr':_ai_ip})
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf', 'db', {'location': _ai_ip})
    else:
        sqlite_cur.execute("update setting set val='0' where name='Co_server'")
        sqlite_cur.execute("update setting set val='0' where name='ai_ip'")
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf', 'ucmq', {'server_addr': ''})
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf', 'db', {'location': ''})
        fp.write("python udpbroad0.pyc &\n")

    if '1' != _ai_f:
        sqlite_cur.execute("update setting set val='0' where name='ai_f'")
        fp.write("python amqp_consumer.pyc &\n")
    else:
        sqlite_cur.execute("update setting set val='1' where name='ai_f'")
    if '0' != _vlpr_f:
        sqlite_cur.execute("update setting set val='1' where name='vlpr_f'")
    else:
        sqlite_cur.execute("update setting set val='0' where name='vlpr_f'")
        fp.write("python amqp_bind.pyc &\n")
    fp.write("""python configfiles.pyc &
sleep 7
python multi_ucmq.pyc &
python rmfiles.pyc &
python auto_reboot.pyc &
python led_displayer.pyc &\n""")
    if '0' == _ai_f:
        fp.write("python ai2filter.pyc &\npython aifilter.pyc &\npython Ai2Lamp.pyc &\npython set_lamp.pyc &\n")
    if '0' == _vlpr_f:
        fp.write('python yuvfilter.pyc &\npython ai2getyuv.pyc &\n')
    if '0' == _h264_f:
        sqlite_cur.execute("update setting set val='0' where name='h264_f'")
        fp.write("python mrtsp.pyc &\n")
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf', 'file_save', {'keep_moving_video': '0'})
    elif '1' == _h264_f:
        sqlite_cur.execute("update setting set val='1' where name='h264_f'")
        fp.write("python mrtsp.pyc &\n")
        wtclib.set_user_config_from_dict('../../../hvpd/prog/conf/conf.conf', 'file_save', {'keep_moving_video': '1'})
    else:
        sqlite_cur.execute("update setting set val='2' where name='h264_f'")
    fp.write("python wdt.pyc &\n")
    fp.close()
    if 0 == _ctl_ip:
        sqlite_cur.execute("update setting set val='0' where name='ctl_ip'")
    else:
        sqlite_cur.execute("update setting set val='%s' where name='ctl_ip'"%(_ctl_ip))
        wtclib.set_user_config_from_dict('../searchPath/src/conf.ini', 'ctrl', {'server_addr': _ctl_ip})
except Exception,e:
    print e

if 0 != _ai_ip and '0' != _Co_server:
    print """<input type="radio" name="Co_server" value="0">The only Server<br>
	<input type="radio" name="Co_server" value="1" checked>Co-Server,while the master Server ip is <input type="text" 
	name="ai_ip" size="20" MAXLENGTH="20" value="%s"><br>"""%_ai_ip
else:
    print """<input type="radio" name="Co_server" value="0" checked>The only Server<br>
	<input type="radio" name="Co_server" value="1">Co-Server,while the master Server ip is <input type="text" 
	name="ai_ip" size="20" MAXLENGTH="20"><br>"""
print "<br><li><h3>Bays check with AI</h3></li>"

if '1' != _ai_f:
    print """<input type="radio" name="ai_f" value="0" checked>OPEN,Graphics card is need<br>
        <input type="radio" name="ai_f" value="1">CLOSE,normally not this<br>"""
else:
    print """<input type="radio" name="ai_f" value="0">OPEN,Graphics card is need<br>
        <input type="radio" name="ai_f" value="1" checked>CLOSE,normally not this<br>"""

print "<li><h3>VLPR function</h3></li>"

if '0' != _vlpr_f:
    print """<input type="radio" name="vlpr_f" value="0">OPEN<br>
    <input type="radio" name="vlpr_f" value="1" checked>CLOSE, for less CPU usage<br>"""
else:
    print """<input type="radio" name="vlpr_f" value="0" checked>OPEN<br>
    <input type="radio" name="vlpr_f" value="1">CLOSE, for less CPU usage<br>"""

print "<li><h3>H264 motion video</h3></li>"

if '0' == _h264_f:
    print """<input type="radio" name="h264_f" value="0" checked>A NVR with this Server, only coming and going,less HDD used, *recommend<br>
<input type="radio" name="h264_f" value="1">A NVR with this Server, every motion,more HDD used,and maybe not enough channel for a coming or going<br>
<input type="radio" name="h264_f" value="2">Another equipment NVR with onvif protocol,port 80, user and psw is none<br>"""
elif '1' == _h264_f:
    print """<input type="radio" name="h264_f" value="0">A NVR with this Server, only coming and going,less HDD used, *recommend<br>
<input type="radio" name="h264_f" value="1" checked>A NVR with this Server, every motion,more HDD used,and maybe not enough channel for a coming or going<br>
<input type="radio" name="h264_f" value="2">Another equipment NVR with onvif protocol,port 80, user and psw is none<br>"""
else:
    print """<input type="radio" name="h264_f" value="0">A NVR with this Server, only coming and going,less HDD used, *recommend<br>
<input type="radio" name="h264_f" value="1">A NVR with this Server, every motion,more HDD used,and maybe not enough channel for a coming or going<br>
<input type="radio" name="h264_f" value="2" checked>Another equipment NVR with onvif protocol,port 80, user and psw is none<br>"""

print "<li><h3>Search my car</h3></li>"
if 0 == _ctl_ip:
    print """The parkGuide/indexPage.html Server ip is <input type="text" name="ctl_ip" size="20" MAXLENGTH="20"></ul>"""
else:
    print """The parkGuide/indexPage.html Server ip is <input type="text" name="ctl_ip" size="20" MAXLENGTH="20" value="%s"></ul>"""%_ctl_ip

print """<h3><font color="#FF0000">Notice: after Modify button click, You must reboot this Server manually, and all setting will be OK.</font></h3>
<input name ="UserSetA" type="submit" value="Modify" onClick="alert('Succeed')">
<input name="FacDefaultA" type="submit" value="Use Factory Settings"onClick="alert('Set as Factory Settings')">
</form>
</body>
</html>"""
