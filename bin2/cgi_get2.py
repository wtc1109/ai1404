#!/usr/bin/python
import cgi, json
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
           "sn char(32) primary key," \
           "imei char(64)," \
           "warning char(64)," \
           "gsm_rssi int," \
           "pos_lat double," \
           "pos_lng double," \
           "Vbatt_mv int," \
           "val char(128)," \
           "connect_time datetime" \
           ");"
    sqlite_cur.execute(_sql)

    form = cgi.FieldStorage()
    _dict1 = {"ret":"ok"}
    for key in form.keys():
        _dict1.update({key:form[key].value})
    #_dict1.update({'sn':'123','warning':'low'})
    if 'sn' in _dict1:
        _imei = ''
        _gsm = '0'
        _lat = '40.0'
        _lng = '119.0'
        _val = ''
        _warning = ''
        _vBatt = '0'
        if 'imei' in _dict1:
            _imei = _dict1['imei']
        if 'lat' in _dict1:
            _lat = _dict1['lat']
        if 'lng' in _dict1:
            _lng = _dict1['lng']
        if 'warning' in _dict1:
            _warning = _dict1['warning']
        if 'gsm' in _dict1:
            _gsm = _dict1['gsm']
        if 'val' in _dict1:
            _val = _dict1['val']
        if 'batt' in _dict1:
            _vBatt = _dict1['batt']

        _sql = "select sn from online where sn='%s'"%_dict1['sn']
        sqlite_cur.execute(_sql)
        if len(sqlite_cur.fetchall()) > 0:
            _sql = "update online set imei='%s',warning='%s',gsm_rssi=%s,pos_lat=%s,pos_lng=%s,Vbatt_mv=%s,val='%s'," \
                   "connect_time=datetime('now') where sn='%s'"%(_imei, _warning, _gsm,_lat,_lng,_vBatt,_val, _dict1['sn'])
        else:
            _sql = "insert into online(sn, imei,warning,gsm_rssi,pos_lat,pos_lng,Vbatt_mv,val,connect_time)values" \
                   "('%s','%s','%s',%s,%s,%s,%s,'%s',datetime('now'))"%(_dict1['sn'], _imei,_warning,_gsm,_lat,_lng,_vBatt,_val)
        sqlite_cur.execute(_sql)
    print "Content-type:text/html\n\n"
    print json.dumps(_dict1)