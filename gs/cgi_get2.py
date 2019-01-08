#!/usr/bin/python
import cgi, json,time
import sqlite3

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
    sqlite_cur, hvpd_conn = get_sqlite_cur("imei.db")
    _sql = "create table if not exists online(" \
           "imei char(32) primary key," \
           "sn char(32)," \
           "warning char(64)," \
           "gsm_rssi int," \
           "Vbatt_mv int," \
           "val char(128)," \
           "connect_time datetime," \
		   "life int default 1," \
           "mcc int default 0," \
           "mnc int default 0," \
           "lac int default 0," \
           "ci int default 0," \
           "need_upgrade int default 0," \
           "userID int default 0," \
           "softVersion char(16)" \
           ");"
    sqlite_cur.execute(_sql)

    form = cgi.FieldStorage()
    _dict1 = {"ret":"ok"}
    for key in form.keys():
        _dict1.update({key:form[key].value})
    _dict1.update({'imei':'125634','sn':'1234','warning':'low','val':'460.01.6311.49234.30;460.01.6311.49233.23;460.02.6322.49232.18;'})
    if 'sn' in _dict1:
        _imei = '12345'
        _gsm = '0'
        _val = ''
        _warning = ''
        _vBatt = '0'
        mcc = '0'
        mnc = '0'
        lac = '0'
        ci = '0'
        if 'imei' in _dict1:
            _imei = _dict1['imei']
        if 'warning' in _dict1:
            _warning = _dict1['warning']
        if 'gsm' in _dict1:
            _gsm = _dict1['gsm']
        if 'val' in _dict1:
            _val = _dict1['val']
            CellInfoExt = _val.split(';')
            _val = CellInfoExt[0]
            if len(_val) != 0:
                _info = _val.split('.')
                mcc = _info[0]
                mnc = _info[1]
                lac = _info[2]
                ci = _info[3]
            sqlite_cur2, hvpd_conn2 = get_sqlite_cur("cellinfo.db")
            _sql = "create table if not exists cellinfo(" \
                   "mcc int," \
                   "mnc int," \
                   "lac int," \
                   "ci int," \
                   "rssi int," \
                   "pos_lat double default 100.0,"\
                   "pos_lng double default 0.0," \
                   "radius int default 0," \
                   "addr char(128)," \
                   "try_times int default 0," \
                   "primary key (mcc,mnc,lac,ci)" \
                   ");"#never lat bigger than 90
            sqlite_cur2.execute(_sql)
            for _cellinfo1 in CellInfoExt:
                if len(_cellinfo1) == 0:
                    continue
                _cellinfo = _cellinfo1.split('.')
                _sql = "select pos_lat from cellinfo where mcc=%s and mnc=%s and lac=%s and ci=%s"\
                       %(_cellinfo[0],_cellinfo[1],_cellinfo[2],_cellinfo[3])
                sqlite_cur2.execute(_sql)
                if None == sqlite_cur2.fetchone():
                    _sql = "insert into cellinfo (mcc,mnc,lac,ci,rssi)values(%s,%s,%s,%s,30)"%(_cellinfo[0],_cellinfo[1],_cellinfo[2],_cellinfo[3])
                    sqlite_cur2.execute(_sql)
            hvpd_conn2.close()
        if 'batt' in _dict1:
            _vBatt = _dict1['batt']

        _sql = "select life from online where imei='%s'"%_imei
        try:
            sqlite_cur.execute(_sql)
            _life_t = sqlite_cur.fetchone()
            if None != _life_t:
                _life = _life_t[0]
                _sql = "update online set warning='%s',gsm_rssi=%s,Vbatt_mv=%s,val='%s'," \
                       "connect_time=datetime('now'),life=%d,mcc=%s,mnc=%s,lac=%s,ci=%s where imei='%s'"\
                       %(_warning, _gsm,_vBatt,_val,_life+1,mcc,mnc,lac,ci,_imei)
            else:
                _sql = "insert into online(sn, imei,warning,gsm_rssi,Vbatt_mv,val,connect_time," \
                       "mcc,mnc,lac,ci)values('%s','%s','%s',%s,%s,'%s',datetime('now'),%s,%s,%s,%s)"\
                       %(_dict1['sn'], _imei,_warning,_gsm,_vBatt,_val,mcc,mnc,lac,ci)
                _life = 1
            sqlite_cur.execute(_sql)

        except Exception, e:
            print _dict1.update({'err':str(e)})
        hvpd_conn.close()
        localtime1 = time.localtime()
        _logdb = "log%d%02d.db"%(localtime1.tm_year, localtime1.tm_mon)
        sqlite_cur, hvpd_conn = get_sqlite_cur(_logdb)
        _sql = "create table if not exists log(" \
               "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
               "imei char(32)," \
               "warning char(64)," \
               "gsm_rssi int," \
               "Vbatt_mv int," \
               "val char(128)," \
               "connect_time datetime," \
               "life int default 1," \
               "mcc int default 0," \
               "mnc int default 0," \
               "lac int default 0," \
               "ci int default 0" \
               ");"
        sqlite_cur.execute(_sql)
        _sql = "insert into log values" \
               "(NULL,'%s','%s',%s,%s,'%s',datetime('now'),%d,%s,%s,%s,%s)"\
               %(_imei,_warning,_gsm,_vBatt,_val,_life+1,mcc,mnc,lac,ci)
        sqlite_cur.execute(_sql)
        if '' != _warning:
            _sql = "create table if not exists warning(" \
                   "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
                   "imei char(32)," \
                   "warning char(64)," \
                   "gsm_rssi int," \
                   "Vbatt_mv int," \
                   "val char(128)," \
                   "connect_time datetime," \
                   "life int default 1," \
                   "mcc int default 0," \
                   "mnc int default 0," \
                   "lac int default 0," \
                   "ci int default 0" \
                   ");"
            sqlite_cur.execute(_sql)
            _sql = "insert into warning values(null,'%s','%s',%s,%s,'%s',datetime('now'),%d,%s,%s,%s,%s)"\
                   %(_imei,_warning,_gsm,_vBatt,_val,_life+1,mcc,mnc,lac,ci)
            sqlite_cur.execute(_sql)
    hvpd_conn.close()
    print "Content-type:application/json\r\n\r\n"
    print json.dumps(_dict1)