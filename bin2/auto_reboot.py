import os, time,sqlite3,wtclib
import socket
import hvpd_status

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


def get_a_sql_cur_forever():
    global mylogger
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylogger.info(err)
            time.sleep(20)
    return _cur

if __name__ == '__main__':
    if not os.path.isdir("../log/auto_reboot"):
        try:
            os.mkdir("../log/auto_reboot")
        except Exception, e:
            print str(e)
            os._exit()
    mylogger = wtclib.create_logging("../log/auto_reboot/auto_reboot.log")
    mylogger.info("start running")
    os.remove("hvpd.db")
    os.remove("rebootlog.db")
    sqlite_cur, hvpd_conn = get_sqlite_cur("hvpd.db")
    reboot_Log_cur, log_conn = get_sqlite_cur("rebootlog.db")
    _sql = "create table if not exists hvpdOnline(" \
           "cameraID char(24)," \
           "cmosID int," \
           "ip char(20)," \
           "reboot_timet int," \
           "reboot_time datetime," \
           "primary key(cameraID, cmosID)" \
           ");"
    sqlite_cur.execute(_sql)

    _sql = "create table if not exists hvpdlog(" \
           "id integer primary key autoincrement," \
           "cameraID char(24) ," \
           "cmosID int," \
           "ip char(20)," \
           "reboot_time datetime," \
           "AISERVERIP char(20)," \
           "cgi_timenow char(20)," \
           "ret_postfile char(20)," \
           "ret_cgi_msg2device char(20)" \
           ");"
    reboot_Log_cur.execute(_sql)
    #reboot_Log_cur.execute("insert into hvpdlog(reboot_time)values(datetime('now','localtime'))")
    log_conn.close()

    mysql_cur = get_a_sql_cur_forever()
    try:
        a1 = mysql_cur.execute("select * from onlinehvpdstatustablemem")
        sqlite_cur, hvpd_conn = get_sqlite_cur("hvpd.db")
        mylogger.info("Get %d hvpds from Mysql DB"%a1)
        _hvpds = mysql_cur.fetchmany(a1)
        for _hvpd in _hvpds:

            _sql = "select * from hvpdOnline where cameraID='%s' and cmosID=%d;"%(_hvpd[0], _hvpd[1])
            sqlite_cur.execute(_sql)
            _NewHvpd = sqlite_cur.fetchone()
            if None == _NewHvpd:
                sqlite_cur.execute("insert into hvpdOnline(cameraID, cmosID, ip, reboot_timet)values('%s',%d,'%s',%d)"%(
                    _hvpd[0],_hvpd[1],_hvpd[4],_hvpd[10]))
                #mylogger.debug("timet=%d"%_hvpd[10])
    except Exception, e:
        mylogger.error(str(e))
    hvpd_conn.close()
    while True:
        _timeNow = int(time.time())
        _dic1 = {"reboot":1}
        reboot_Log_cur, log_conn = get_sqlite_cur("rebootlog.db")
        sqlite_cur, hvpd_conn = get_sqlite_cur("hvpd.db")
        try:
            a1 = mysql_cur.execute("select * from onlinehvpdstatustablemem where length(ip)!=0")
            mylogger.info("Get %d hvpds from Mysql DB"%a1)
            _hvpds = mysql_cur.fetchmany(a1)
            for _hvpd in _hvpds:
                if _timeNow - _hvpd[10] < 20*60:
                    _sql = "update hvpdOnline set reboot_timet=%d, reboot_time=datetime('now','localtime') " \
                           "where cameraID='%s' and cmosID=%d;"%(_hvpd[10],_hvpd[0],_hvpd[1])
                    sqlite_cur.execute(_sql)
                    #mylogger.debug("update timet = %d"%_hvpd[10])
                    continue
                _sql = "select * from hvpdOnline where cameraID='%s' and cmosID=%d;" % (_hvpd[0], _hvpd[1])
                sqlite_cur.execute(_sql)
                _NewHvpd = sqlite_cur.fetchone()
                if _timeNow - _NewHvpd[3] > 20*60:
                    mylogger.info("sn=%s cmos %d need reboot @ %s" % (_hvpd[0], _hvpd[1], _hvpd[4]))
                    try:
                        _status_url = "http://" + _hvpd[4] + "/cgi-bin/status.cgi"
                        socket.setdefaulttimeout(2)
                        _status_dict = hvpd_status.get_hvpd_status(_status_url)
                        mylogger.info("get_hvpd_status ")
                        _ai_ip = "None"
                        _cgi_time = "None"
                        if None != _status_dict:
                            if "AISERVERIP" in _status_dict:
                                _ai_ip = _status_dict["AISERVERIP"]
                            if "timenow" in _status_dict:
                                _cgi_time = _status_dict["timenow"]

                        ret_file = wtclib.http_post_file2device("reboot_upgrade.zip", _hvpd[4], "upgrade.cgi")
                        mylogger.info("post file")
                        if 200 == ret_file:
                            _post_file = "OK"
                        else:
                            _post_file = "failt"
                        ret, err = wtclib.http_get_cgi_msg2device(_dic1, _hvpd[4], "setting")
                        mylogger.info("http_get_cgi_msg2device")
                        if 1 != ret:
                            _cgi_msg2device = "failt"
                        else:
                            _cgi_msg2device = "OK"
                        _sql = "insert into hvpdlog(cameraID,cmosID,ip,reboot_time,AISERVERIP,cgi_timenow,ret_postfile,ret_cgi_msg2device )" \
                               "values('%s',%d,'%s',datetime('now','localtime'),'%s','%s','%s','%s')"\
                               %(_hvpd[0],_hvpd[1],_hvpd[4],_ai_ip,_cgi_time,_post_file,_cgi_msg2device)
                        reboot_Log_cur.execute(_sql)
                        sqlite_cur.execute(
                            "update hvpdOnline set reboot_timet=%d, reboot_time=datetime('now','localtime') "
                            "where cameraID='%s' and cmosID=%d;" % (_timeNow, _hvpd[0],_hvpd[1]))
                        mylogger.info("write log")
                    except Exception, e:
                        mylogger.error(str(e))



            sqlite_cur.execute("select * from hvpdOnline where reboot_timet<%d;"%(_timeNow - 20*60))
            _hvpds = sqlite_cur.fetchall()
            if None != _hvpds:
                mylogger.info("Get %d hvpds from hvpdOnline DB reboot_timet > 20*60sec"%(len(_hvpds)))
                for _hvpd in _hvpds:
                    mylogger.info("sn%s cmos %d need reboot @ %s"%(_hvpd[0],_hvpd[1],_hvpd[2]))
                    try:
                        _status_url = "http://" + _hvpd[2] + "/cgi-bin/status.cgi"
                        socket.setdefaulttimeout(2)
                        _status_dict = hvpd_status.get_hvpd_status(_status_url)
                        mylogger.info("get_hvpd_status")
                        _ai_ip = "None"
                        _cgi_time = "None"
                        if None != _status_dict:
                            if "AISERVERIP" in _status_dict:
                                _ai_ip = _status_dict["AISERVERIP"]
                            if "timenow" in _status_dict:
                                _cgi_time = _status_dict["timenow"]

                        ret_file = wtclib.http_post_file2device("reboot_upgrade.zip", _hvpd[2], "upgrade.cgi")
                        mylogger.info("http_post_file2device")
                        if 200 == ret_file:
                            _post_file = "OK"
                        else:
                            _post_file = "failt"
                        ret, err = wtclib.http_get_cgi_msg2device(_dic1, _hvpd[2], "setting")
                        mylogger.info("http_get_cgi_msg2device")
                        if 1 != ret:
                            _cgi_msg2device = "failt"
                        else:
                            _cgi_msg2device = "OK"
                        _sql = "insert into hvpdlog(cameraID,cmosID,ip,reboot_time,AISERVERIP,cgi_timenow,ret_postfile,ret_cgi_msg2device )" \
                               "values('%s',%d,'%s',datetime('now','localtime'),'%s','%s','%s','%s')"\
                               %(_hvpd[0],_hvpd[1],_hvpd[2],_ai_ip,_cgi_time,_post_file,_cgi_msg2device)
                        reboot_Log_cur.execute(_sql)
                        sqlite_cur.execute(
                            "update hvpdOnline set reboot_timet=%d, reboot_time=datetime('now','localtime')"
                            "where cameraID='%s' and cmosID=%d;" % (_timeNow, _hvpd[0],_hvpd[1]))
                        mylogger.info("write log")
                    except Exception, e:
                        mylogger.error(str(e))


            else:
                mylogger.info("Get None from hvpd.db reboot time > 20*60")


        except Exception, e:
            mylogger.error(str(e))
            if 'MySQL server has gone away' in str(e):
                mysql_cur = get_a_sql_cur_forever()

        log_conn.close()
        hvpd_conn.close()
        mylogger.debug("reboot use %f sec"%(time.time() - _timeNow))
        time.sleep(5*60)