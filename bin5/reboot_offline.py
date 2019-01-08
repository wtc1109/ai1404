import wtclib
import time

def get_a_sql_cur_forever():
    global mylogger
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != _cur:
            break
        else:
            mylogger.info(err)
            time.sleep(20)
    return _cur

if __name__ == '__main__':
    cur = get_a_sql_cur_forever()
    _sql_str = "select * from camera_ipaddrsettingtable"
    cur.execute(_sql_str)
    _all_hvpds = cur.fetchall()
    for _hvpd in _all_hvpds:
        _sql_str = "select * from onlinehvpdstatustablemem where cameraID='%s'"%_hvpd[0]
        if 0 != cur.execute(_sql_str):
            _hvpd1 = cur.fetchone()
            if None != _hvpd1[4]:
                continue

        wtclib.http_post_file2device("reboot_upgrade.zip", _hvpd[6], "upgrade.cgi")
        print "reboot "+ _hvpd[0]