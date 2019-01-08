import urllib2, json,sqlite3, time

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

if __name__ == '__main__':
    sqlite_cur2, hvpd_conn2 = get_sqlite_cur("cellinfo.db")
    while True:
        _sql = "select * from cellinfo where pos_lat>90 and try_times<100"
        sqlite_cur2.execute(_sql)
        _all_infos = sqlite_cur2.fetchall()
        if None != _all_infos:
            for _info in _all_infos:
                try:
                    _str = "http://api.cellocation.com:81/cell/?mcc=%d&mnc=%d&lac=%d&ci=%d&output=json"\
                           %(_info[0],_info[1],_info[2],_info[3])
                    req = urllib2.Request(_str)
                    _ret = urllib2.urlopen(req, timeout=2)
                    res = _ret.read()
                    _save_info = json.loads(res)
                    if not 'errcode' in _save_info:
                        continue
                    if _save_info["errcode"] != 0:
                        _sql = "update cellinfo set try_times=%d where mcc=%d and mnc=%d and lac=%d and ci=%d"\
                               %(_info[9]+1,_info[0], _info[1], _info[2], _info[3])
                        sqlite_cur2.execute(_sql)
                        continue
                    if not 'lat' in _save_info:
                        continue

                    _sql = "update cellinfo set pos_lat=%s,pos_lng=%s,radius=%s,addr='%s' where " \
                           "mcc=%d and mnc=%d and lac=%d and ci=%d"\
                           %(_save_info['lat'],_save_info['lon'],_save_info['radius'],_save_info['address'].encode('gbk').decode('gbk'),
                             _info[0], _info[1], _info[2], _info[3])
                    sqlite_cur2.execute(_sql)
                except Exception,e:
                    print e
        time.sleep(20)