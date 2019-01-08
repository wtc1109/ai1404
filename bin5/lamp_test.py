import os, time,wtclib,socket

if __name__ == '__main__':
    while True:
        _cur, _conn = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None == _cur:
            time.sleep(5)
        else:
            break
    print "DB connect OK"
    while True:
        print "********"
        try:
            a1 = _cur.execute("select * from OnlineHvpdStatusTableMem")
            _hvpds = _cur.fetchmany(a1)
            socket.setdefaulttimeout(1)
            try:
                for _hvps in _hvpds:
                    if None == _hvps[4]:
                        continue
                    wtclib.http_get_cgi_msg2device({"Lamp": "R:0,G:20,B:0"}, ip=_hvps[4],cgi_name="setting")
                    print "%s is Green"%_hvps[4]
            except Exception, e:
                print str(e)
            time.sleep(5)
            try:
                for _hvps in _hvpds:
                    if None == _hvps[4]:
                        continue
                    wtclib.http_get_cgi_msg2device({"Lamp": "R:0,G:0,B:20"}, ip=_hvps[4],cgi_name="setting")
                    print "%s is Blue" % _hvps[4]
            except Exception, e:
                print str(e)
            time.sleep(5)
            for _hvps in _hvpds:
                if None == _hvps[4]:
                    continue
                wtclib.http_get_cgi_msg2device({"Lamp": "R:20,G:0,B:0"}, ip=_hvps[4],cgi_name="setting")
                print "%s is Red" % _hvps[4]
            time.sleep(5)
        except Exception, e:
            print str(e)