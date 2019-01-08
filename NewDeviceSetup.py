import urllib, urllib2, time, json
import os,sys
import socket
import pika
import MySQLdb
import Queue
import threading
from bin import wtclib
import ConfigParser
import math

mylogger = wtclib.create_logging("NewDeviceSetup.log")
mylogger.info("start running")

def ucmq_get_msg(ucmq_url):
    global mylogger
    while True:
        while True:
            try:
                res_data = urllib2.urlopen(ucmq_url)
                break
            except urllib2.URLError, e:
                print str(e) + " in line: " + str(sys._getframe().f_lineno)
                mylogger.info(str(e))
                time.sleep(20)
                continue
        res = res_data.read()
        mq_str = res.split('\n')
        #print mq_str[0]
        ret_str = mq_str[0].rstrip('\r')
        if (ret_str != "UCMQ_HTTP_OK"):
            mq_str[1] = None
        res_data.close()
        break

    urllib.urlcleanup()
    return mq_str[1]

if __name__ == '__main__':

    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="Producer")
        conn.autocommit(1)
        cur = conn.cursor()
    except:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456")
        conn.autocommit(1)
        cur = conn.cursor()
        cur.execute("create database Producer")
        cur.execute("use Producer")

    try:
        cur.execute("create table if not exists DeviceTable("
                    "CPUID char(24) primary key, "
                    "neighbor_CPUID char(24),"
                    "MAC_Set char(24),"
                    "cameraID char(24),"

                    "product_time DATETIME, "
                    "time_int int"
                    ")")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        pass
    try:
        cur.execute("create table if not exists newDeviceTable("
                    "CPUID char(24) primary key, "
                    "neighbor_CPUID char(24),"
                    "Setup_flag tinyint,"
                    "ip char(24),"
                    "MAC_Set char(24),"
                    "cameraID char(24)"
                    ")engine=memory")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        pass
    _time_sec = int(time.time())
    try:
        cur.execute("insert into DeviceTable(CPUID, MAC_Set, cameraID, product_time, time_int)values('123456789abc', '00-1b-3c-00-11-22', '1610430123', now(), %d)"%_time_sec)
        cur.execute(
            "insert into DeviceTable(CPUID, MAC_Set, cameraID, product_time, time_int)values('123456789abc1', '00-1B-3C-00-11-23', '1610430124', now(), %d)"%_time_sec)
        cur.execute("insert into newDeviceTable(CPUID, neighbor_CPUID, Setup_flag)values('123456', '123457', 1)")
    except:
        pass
    while True:
        (_val, _ucmq_url) = wtclib.get_ucmq_url("setupmq")
        if 0 == _val:
            print "get ucmq error "+_ucmq_url
        else:
            break
    while True:

        _json_str = ucmq_get_msg(_ucmq_url)
        if None == _json_str:
            time.sleep(0.5)
            continue
        _ucmq_dic = json.loads(_json_str)
        if not "sn" in _ucmq_dic:
            continue
        if len(_ucmq_dic["sn"]) > 10:
            b1 = cur.execute("select * from DeviceTable where CPUID='%s'" % _ucmq_dic["sn"])
            if 0 != b1:
                _camera_info = cur.fetchmany(1)[0]
                _dic_msg_set = {"FMAC": _camera_info[2], "Fsn": _camera_info[3], "reboot": 1}
                (_val, _err) = wtclib.http_get_cgi_msg2device(_dic_msg_set, _ucmq_dic["ip"], cgi_name="setting")
                continue
            a1 = cur.execute("select * from newDeviceTable where CPUID='%s'"%_ucmq_dic["sn"])
            if 0 != a1:
                _new_dev = cur.fetchmany(a1)[0]
                if 1 != _new_dev[2]:
                    b1 = cur.execute("select * from DeviceTable where CPUID='%s'"%_ucmq_dic["sn"])
                    if 0 == b1:
                        cur.execute("update newDeviceTable set Setup_flag=%d, where CPUID='%s'"%(_new_dev[2]+3, _ucmq_dic["sn"]))
                        continue
                    _dev_db = cur.fetchmany(b1)[0]
                    _dic_msg_set = {"FMAC": _dev_db[2], "Fsn": _dev_db[3], "reboot":1}
                    (_val, _err) = wtclib.http_get_cgi_msg2device(_dic_msg_set, _ucmq_dic["ip"], cgi_name="setting")
                elif _new_dev[2] > 20:  #too many errors
                    cur.execute("delete from newDeviceTable where CPUID='%s'"%_ucmq_dic["sn"])
                continue

            _localTime = time.localtime()
            _year = _localTime.tm_year - 2000
            _mon = _localTime.tm_mon
            _old_dev = cur.fetchmany(cur.execute("select * from DeviceTable where cameraID=(select max(cameraID) as cameraID from DeviceTable)"))[0]
            _year_mon = "%02d%02d"%(_year, _mon)
            if _year_mon  == _old_dev[3][0:4]:
                _len_sn = len(_old_dev[3])
                _sn_int = int(_old_dev[3][_len_sn-4: _len_sn])
            else:
                _sn_int = 2
            if 0 != (_sn_int%2):
                _sn_int += 1
            else:
                _sn_int += 2
            _sn_str = "%s43%04d" % (_year_mon, _sn_int)
            _mac_list = _old_dev[2].split('-')
            _mac_hex = int("%s%s%s" % (_mac_list[3], _mac_list[4], _mac_list[5]), 16)
            _mac_hex += 1
            _mac_hex1 = "%06X" % (_mac_hex)
            _mac_str = "%s-%s-%s-%s-%s-%s" % (
            _mac_list[0], _mac_list[1], _mac_list[2], _mac_hex1[:2], _mac_hex1[2:4], _mac_hex1[4:6])
            _dic_msg_set = {"FMAC": _mac_str, "Fsn": _sn_str, "reboot":1}
            (_val, _err) = wtclib.http_get_cgi_msg2device(_dic_msg_set, _ucmq_dic["ip"], cgi_name="setting")
            if 1 != _val:
                continue
            _time_sec = int(time.time())
            if not "neighbor" in _ucmq_dic:

                cur.execute("insert into newDeviceTable(CPUID, Setup_flag)values('%s',1)"%_ucmq_dic["sn"])
                cur.execute("insert into DeviceTable(CPUID, MAC_Set, cameraID, product_time, time_int)values('%s', '%s', '%s', now(), %d)"
                            %(_ucmq_dic["sn"], _mac_str, _sn_str, _time_sec))
            else:

                cur.execute("insert into newDeviceTable(CPUID, neighbor_CPUID, Setup_flag)values('%s','%s',1)"
                            % (_ucmq_dic["sn"], _ucmq_dic["neighbor"]))
                cur.execute(
                    "insert into newDeviceTable(CPUID, neighbor_CPUID, Setup_flag)values('%s','%s',0)"
                    % (_ucmq_dic["neighbor"], _ucmq_dic["sn"]))

                if _ucmq_dic["sn"] == min(_ucmq_dic["sn"], _ucmq_dic["neighbor"]):
                    cur.execute("insert into DeviceTable(CPUID, neighbor_CPUID, MAC_Set, cameraID, product_time, time_int)"
                                "values('%s', '%s', '%s','%s', now(), %d)" % (
                                _ucmq_dic["sn"], _ucmq_dic["neighbor"],_mac_str, _sn_str, _time_sec))
                else:
                    cur.execute(
                        "insert into DeviceTable(CPUID, neighbor_CPUID, MAC_Set, cameraID, product_time, time_int)"
                        "values('%s', '%s', '%s', '%s', now(), %d)" % (
                        _ucmq_dic["neighbor"], _ucmq_dic["sn"], _mac_str, _sn_str, _time_sec))
                _sn_int += 1
                _sn_str = "%s43%04d" % (_year_mon, _sn_int)
                _mac_hex += 1
                _mac_hex1 = "%06X" % (_mac_hex)
                _mac_str = "%s-%s-%s-%s-%s-%s" % (
                    _mac_list[0], _mac_list[1], _mac_list[2], _mac_hex1[:2], _mac_hex1[2:4], _mac_hex1[4:6])

                if _ucmq_dic["sn"] == max(_ucmq_dic["sn"], _ucmq_dic["neighbor"]):
                    cur.execute("insert into DeviceTable(CPUID, neighbor_CPUID, MAC_Set, cameraID, product_time, time_int)"
                                "values('%s', '%s','%s', '%s', now(), %d)" % (
                                _ucmq_dic["sn"], _ucmq_dic["neighbor"],_mac_str, _sn_str, _time_sec))
                else:
                    cur.execute(
                        "insert into DeviceTable(CPUID, neighbor_CPUID, MAC_Set, cameraID, product_time, time_int)"
                        "values('%s', '%s','%s', '%s', now(), %d)" % (
                        _ucmq_dic["neighbor"], _ucmq_dic["sn"], _mac_str, _sn_str, _time_sec))

        time.sleep(0.2)