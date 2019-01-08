import wtclib
import os, time, sys
import socket
import threading
import random
import MySQLdb
import Queue
import json
import datetime
import urllib, urllib2
from HTMLParser import HTMLParser


def update_screen_connect_sql(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return
    try:
        print "update_screen_connect_sql"
        cnt = 0
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                if 3 != len(list1):
                    continue
                cur.execute("insert into ScreenConnectTable(ScreenSn, ScreenName) "
                            "values('%s', '%s')ON DUPLICATE KEY UPDATE ScreenName='%s'"
                            %(list1[1], list1[2], list1[2]))
                cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    return

def update_screen2_connect_sql(path, cur):

    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return

    try:
        print "update_screen2_connect_sql"
        cnt = 0
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                if 5 != len(list1):
                    continue
                cur.execute("insert into ScreenConnectTable(ScreenSn, ScreenName) "
                            "values('%s', '%s')ON DUPLICATE KEY UPDATE ScreenName='%s'"
                            %(list1[1], list1[2], list1[2]))
                try:
                    _len = int(list1[3])
                    _flag = int(list1[4])
                except:
                    _len = 0
                    _flag = 0
                cur.execute("insert into ScreenConfigTable(ScreenSn, RegionNum_len,specialFlag) "
                            "values('%s', %d,%d)ON DUPLICATE KEY UPDATE RegionNum_len=%d, specialFlag=%d"
                            % (list1[1], _len, _flag, _len, _flag))
                cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    return

def update_screen_config(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return

    try:
        print "update_screen_config"
        cnt = 0
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')

                cur.execute("insert into ScreenConfigTable(ScreenSn, CtrlMode, Weight, height, AllRegion) "
                            "values('%s', %s, %s, %s, %s)ON DUPLICATE KEY UPDATE CtrlMode=%s, "
                            "Weight=%s, height=%s, AllRegion=%s"
                            ""%(list1[0], list1[1], list1[2], list1[3], list1[4], \
                                list1[1], list1[2], list1[3], list1[4]))
                for i in range(int(list1[4])):
                    _region = list1[5+i].split(',')
                    cur.execute("update ScreenConfigTable set Region%d = %s"
                                " where ScreenSn='%s'"
                                "" % (i+1, _region[8], list1[0]))
                for _RegionInfo in list1[5:]:
                    if 0 == len(_RegionInfo):
                        break
                    _region = _RegionInfo.split(',')
                    cur.execute("insert into ScreenRegionConfigTable(TopLeftX, TopLeftY, BottomRightX, "
                            "BottomRightY, Action, Font, Color, Display, RegionSn) "
                            "values(%s, %s, %s, %s, %s, %s, %s, '%s', %s)ON DUPLICATE KEY UPDATE "
                            "TopLeftX=%s, TopLeftY=%s, BottomRightX=%s, BottomRightY=%s,"
                            "Action=%s, Font=%s, Color=%s, Display='%s'"% (_region[0], _region[1], _region[2], _region[3], _region[4], _region[5], _region[6],
                                  _region[7], _region[8], _region[0], _region[1], _region[2], _region[3], _region[4],
                                  _region[5], _region[6],_region[7] ))
                    cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    return

def update_screen2_config(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return
    try:
        print "update_screen2_config"
        cnt  = 0
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')

                cur.execute("insert into ScreenConfigTable(ScreenSn, CtrlMode, Weight, height, AllRegion) "
                            "values('%s', %s, %s, %s, %s)ON DUPLICATE KEY UPDATE CtrlMode=%s, "
                            "Weight=%s, height=%s, AllRegion=%s"
                            ""%(list1[0], list1[2], list1[3], list1[4], list1[5],\
                                list1[2], list1[3], list1[4], list1[5]))
                for i in range(int(list1[5])):
                    if len(list1[6+i]) < 5:
                        break
                    _region = list1[6+i].split(',')
                    cur.execute("update ScreenConfigTable set Region%d = %s"
                                " where ScreenSn='%s'"
                                "" % (i+1, _region[8], list1[0]))

                    cur.execute("insert into ScreenRegionConfigTable(TopLeftX, TopLeftY, BottomRightX, "
                            "BottomRightY, Action, Font, Color, Display, RegionSn) "
                            "values(%s, %s, %s, %s, %s, %s, %s, '%s', %s)ON DUPLICATE KEY UPDATE "
                            "TopLeftX=%s, TopLeftY=%s, BottomRightX=%s, BottomRightY=%s,"
                            "Action=%s, Font=%s, Color=%s, Display='%s'"% (_region[0], _region[1], _region[2], _region[3], _region[4], _region[5], _region[6],
                                  _region[7], _region[8], _region[0], _region[1], _region[2], _region[3], _region[4],
                                  _region[5], _region[6],_region[7] ))
                    cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    return


def update_region_config(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return


    try:
        print "update_region_config"
        print time.time()
        cnt = 0
        cur.execute("TRUNCATE TABLE Space2LedTable")
        """
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, CarportStatus) "
                            "values('%s', '%s', 0)ON DUPLICATE KEY UPDATE cameraID='%s'"
                            % (list1[1]+list1[2], list1[1],  list1[1]))
                _sql = "insert into Space2LedTable(id,Spaceid, RegionSn) values('%s','%s', %s)ON DUPLICATE KEY UPDATE " \
                       "RegionSn=%s"% (list1[0]+list1[1] + list1[2],list1[1] + list1[2], list1[0], list1[0])
                cur.execute(_sql)
                cnt += 1
            else:
                break
        """
        _lines = filei.readlines()
        _space_dict = []
        for _line in _lines:
            _line1 = _line.rstrip('\r\n')
            list1 = _line1.split(';')
            Spaceid = list1[1] + list1[2]
            if not Spaceid in _space_dict:
                _space_dict.append(Spaceid)
                cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, CarportStatus) "
                            "values('%s', '%s', 0)ON DUPLICATE KEY UPDATE cameraID='%s'"
                            % (Spaceid, list1[1],  list1[1]))
            _sql = "insert into Space2LedTable(id,Spaceid, RegionSn) values('%s','%s', %s)" \
                   % (list1[0] + list1[1] + list1[2], Spaceid, list1[0])
            cur.execute(_sql)
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    print time.time()
    return


def update_reserved_parking(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return
    try:
        print "update_reserved_parking"
        cnt = 0
        cur.execute("update SpaceStatusTable set reserved=0 where reserved=2")
        while True:
            line = filei.readline()

            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("update SpaceStatusTable set reserved=2 where Spaceid='%s'"%(list1[0]+list1[1]))
                cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "update %d"%cnt
    return


def screen_special_config(path, cur):
    global mylog
    try:
        filei = open(path, 'r')
    except Exception, e:
        mylog.error(str(e))
        return
    try:
        print "screen_special_config"
        cnt = 0
        cur.execute("TRUNCATE TABLE screenspecialconfigtable")
        while True:
            line = filei.readline()

            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                if list1[2].isdigit() and list1[3].isdigit():
                    cur.execute("insert into screenspecialconfigtable(ScreenSn,opt,val1,val2,displayInfo)values"
                            "('%s','%s',%s,%s,'%s')"%(list1[0], list1[1], list1[2], list1[3], list1[4]))
                    cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
    return


def renew_config_info_sql(cur, reNewTime):
    global mylog
    path = "../conf/"

    while not os.path.isdir(path):
        time.sleep(120)
    #(snpath, dirs, filenames), = os.walk(path)
    for snpath, dirs, filenames in os.walk(path):
        print snpath
        break
    try:
        for files in filenames:
            if 0 == files.find("HVCS_region_config"):
                updateTime = os.stat(path + files).st_ctime
                if updateTime > reNewTime:
                    update_region_config(path + files, cur)
                break
        for files in filenames:
            updateTime = os.stat(path + files).st_ctime
            if updateTime <= reNewTime:
                continue
            if 0 == files.find("HVCS_screen_connect"):
                update_screen_connect_sql(path+files, cur)
                continue
            if 0 == files.find("HVCS_screen2_connect"):
                update_screen2_connect_sql(path+files, cur)
                continue
            if 0 == files.find("HVCS_screen_config"):
                update_screen_config(path+files, cur)
                continue
            if 0 == files.find("HVCS_screen2_config"):
                update_screen2_config(path+files, cur)
                continue

            if 0 == files.find("HVCS_reserved_parking"):
                update_reserved_parking(path+files, cur)
                continue
            if 0 == files.find("screenspecialconfigtable"):
                screen_special_config(path+files, cur)
                continue
    except Exception, e:
        mylog.error(str(e))
    return

def check_ip_is_ok(ip_addr):
    try:
        sin = socket.inet_aton(ip_addr)
    except (Exception) as e:
        return -1
    ip_splite = ip_addr.split('.')
    ip_len = len(ip_splite)
    if 4 == ip_len:
        return 0
    else:
        return -2

def fix_hvpd_ip_addr(cur):
    global mylog
    mylog.debug("fix hvpd ip")
    try:
        a1 = cur.execute("select * from hvpdIpAddrSettingTable where ReNewFlag<>0")
        if 0 == a1:
            mylog.debug("0 hvpd fix ip")
            return
        mylog.info("%d hvpds fix ip"%a1)
        try:
            _hvpds = cur.fetchmany(a1)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            return
    except (Exception) as e:
        mylog.error(str(e))
        return
    _pid = os.getpid()

    for _hvpdIP in _hvpds:
        try:
            if 2 == _hvpdIP[2]:
                a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d" % (
                _hvpdIP[0], _hvpdIP[1]))
                if 0 == a1:
                    continue
                _OnlineInfo = cur.fetchmany(1)[0]
                _dic1 = {"Fip": "0", "Fmask": "0", "Frouter": "0", "Fip_set": 0}
                _timeSec = time.time()
                wdi(cur)
                (val, err) = wtclib.http_get_cgi_msg2device(_dic1, ip=_OnlineInfo[4], cgi_name="setting")
                if 0 != val:
                    cur.execute("update hvpdIpAddrSettingTable set ReNewFlag=0, NewIP=NULL,NewMask=NULL,NewGateway=NULL where  cameraID='%s' and cmosID=%d" % (
                    _hvpdIP[0], _hvpdIP[1]))
                continue

            val = 0
            err = "IP Error "
            if None == _hvpdIP[6]:
                val = 3
                err += "ip=None "
            if None == _hvpdIP[7]:
                val = 4
                err += "mask=None "
            if None == _hvpdIP[8]:
                val = 5
                err += "router=None"
            if 0 == val:
                err = ""
            if 0 == val and 0 == check_ip_is_ok(_hvpdIP[6]) and 0 == check_ip_is_ok(_hvpdIP[7]) and 0 == check_ip_is_ok(_hvpdIP[8]):
                a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%(_hvpdIP[0], _hvpdIP[1]))
                if 0 == a1:
                    continue
                _OnlineInfo = cur.fetchmany(1)[0]
                _dic1 = {"Fip":_hvpdIP[6], "Fmask":_hvpdIP[7], "Frouter":_hvpdIP[8], "reboot":1,"Fip_set":1}
                _timeSec = time.time()
                wdi(cur)
                (val, err) = wtclib.http_get_cgi_msg2device(_dic1, ip=_OnlineInfo[4], cgi_name="setting")

            else:
                val = 2
                err = "IP is not good where ip=%s mask=%s router=%s" % (_hvpdIP[6], _hvpdIP[7], _hvpdIP[8])

            if 0 != val:
                cur.execute("update hvpdIpAddrSettingTable set ReNewFlag=0 where  cameraID='%s' and cmosID=%d"%(_hvpdIP[0], _hvpdIP[1]))
                #print "fix %s ip to %s,%s,%s"%(_hvpdIP[0], _hvpdIP[6], _hvpdIP[7], _hvpdIP[8])
                mylog.info("fix %s ip to %s,%s,%s"%(_hvpdIP[0], _hvpdIP[6], _hvpdIP[7], _hvpdIP[8]))

            if "" != err:
                mylog.warning(err)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylog.error(str(e))


def check_and_upgrade_hvpd(cur):
    global mylog
    try:
        a1 = cur.execute("select * from HvpdUpgradeTable where ReNewFlag<>0")
        if 0 == a1:
            mylog.debug("0 hvpd need upgrade firmware")
            return
        mylog.info("%d hvpds need to upgrade firmware"%a1)
        _pid = os.getpid()
        _hvpds = cur.fetchmany(a1)
        for _hvpd in _hvpds:
            if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'and cmosID=0"%(_hvpd[0])):
                continue
            _camera = cur.fetchone()
            if None == _camera:
                continue
            if None == _camera[4]:
                continue
            _timeSec = int(time.time())
            """
            if _timeSec - _camera[10] > 60*60:
                mylog.debug("%s is timeout, last connect time is %s"%(_camera[0],_camera[9]))
                continue
            """
            wdi(cur)
            mylog.info(_hvpd[0]+" upgrade firmware "+_hvpd[2])
            ret = wtclib.http_post_file2device("../../firmwares/" + _hvpd[2], _camera[4], "upgrade.cgi")
            if 200 == ret:
                cur.execute("update HvpdUpgradeTable set ReNewFlag=0, end_time=now() where cameraID='%s' and cmosID=0"%_hvpd[0])
                cur.execute("update HvpdVersionTableMem set renewtimet=0 where cameraID='%s'"%_hvpd[0])

            time.sleep(0.5)
    except Exception, e:
        mylog.debug(str(e))
        pass


def check_and_upgrade_fixip_hvpd(cur):
    global mylog
    try:
        a1 = cur.execute("select * from HvpdUpgradeTable where ReNewFlag<>0")
        if 0 == a1:
            mylog.debug("0 hvpd need upgrade fixip firmware")
            return
        mylog.info("%d fixip hvpds need to upgrade firmware"%a1)
        _pid = os.getpid()
        _hvpds = cur.fetchmany(a1)
        for _hvpd in _hvpds:
            if 0 == cur.execute("select * from hvpdipaddrsettingtable where cameraID='%s'"%(_hvpd[0])):
                continue
            _camera = cur.fetchone()
            if None == _camera:
                continue
            _timeSec = int(time.time())

            wdi(cur)
            mylog.info(_hvpd[0]+" upgrade firmware "+_hvpd[2])
            ret = wtclib.http_post_file2device("../../firmwares/" + _hvpd[2], _camera[6], "upgrade.cgi")
            if 200 == ret:
                cur.execute("update HvpdUpgradeTable set ReNewFlag=0, end_time=now() where cameraID='%s' and cmosID=0"%_hvpd[0])
                cur.execute("update HvpdVersionTableMem set renewtimet=0 where cameraID='%s'"%_hvpd[0])

            time.sleep(0.5)
    except Exception, e:
        mylog.debug(str(e))
        pass


def wdi(cur):
    global mylog,ServerID
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(),ServerID))
    except Exception, e:
        mylog.error(str(e))
        return -1
    return 0


def calc_phase_val(xys):
    xxs = []
    yys = []
    for i in range(0,8,2):
        xxs.append(xys[i])
        yys.append(xys[i+1])
    _maxX1 = xxs.pop(xxs.index(max(xxs)))
    _maxX2 = xxs.pop(xxs.index(max(xxs)))
    _maxY1 = yys.pop(yys.index(max(yys)))
    _maxY2 = yys.pop(yys.index(max(yys)))

    if 0 == _maxX1 or 0 == _maxY1:

        return None
    _LTx = (xxs[0]+xxs[1])/2
    _LTy = (yys[0] + yys[1])/2
    _RBx = (_maxX1 + _maxX2)/2
    _RBy = (_maxY1 + _maxY2)/2
    _strxy = "%d,%d;%d,%d"%(_LTx,_LTy,_RBx,_RBy)
    return _strxy

def calc_phase_val2(xys):
    xxs = []
    yys = []
    for i in range(0, 8, 2):
        xxs.append(xys[i])
        yys.append(xys[i + 1])

    if 0 == max(xxs) or 0 == max(yys):
        return None
    _deltY = int((max(yys)-min(yys))/4)
    _LTy = min(yys)+_deltY
    _RBy = max(yys) - _deltY
    _LTx = xys[0]
    _RBx = xys[2]

    _strxy = "%d,%d;%d,%d" % (_LTx, _LTy, _RBx, _RBy)
    return _strxy


def calc_phase_val3(xys):
    xxs = []
    yys = []
    for i in range(0,8,2):
        xxs.append(xys[i])
        yys.append(xys[i+1])
    _maxX1 = xxs.pop(xxs.index(max(xxs)))
    _maxX2 = xxs.pop(xxs.index(max(xxs)))
    _maxY1 = yys.pop(yys.index(max(yys)))
    _maxY2 = yys.pop(yys.index(max(yys)))

    if 0 == _maxX1 or 0 == _maxY1:

        return None
    _LTx = (xxs[0]+xxs[1])/2
    _LTy = (yys[0] + yys[1])/2
    _RBx = (_maxX1 + _maxX2)/2
    _RBy = (_maxY1 + _maxY2)/2
    _deltY = int((_RBy - _LTy) / 4)
    _LTy += _deltY
    _RBy -= _deltY
    _strxy = "%d,%d;%d,%d"%(_LTx,_LTy,_RBx,_RBy)
    return _strxy


"""renew data in every 30mins"""
def renew_a_hvpd_phaseCheck(hvpd, cur):
    global mylog

    try:
        a1 = cur.execute("select * from AiSettingTableMem where cameraID='%s' and cmosID=%d"%(hvpd[0], hvpd[1]))
        if (0 == a1):
            return
        mylog.debug("renew %s phase check"%hvpd[0])
        _ai_setting = cur.fetchmany(1)[0]
        b1 = cur.execute("select * from AiOutTable where cameraID='%s' and cmosID=%d" % (hvpd[0], hvpd[1]))
        if 0 != b1:
            _ai_out = cur.fetchmany(1)[0]
        else:
            _ai_out = None
        c1 = cur.execute("select * from CameraPhaseCheckSettingTableMem where cameraID='%s' and cmosID=%d" % (hvpd[0], hvpd[1]))
        if 0 == c1:
            cur.execute("insert into CameraPhaseCheckSettingTableMem(cameraID, cmosID)values('%s',%d)" % (hvpd[0], hvpd[1]))
            c1 = cur.execute(
                "select * from CameraPhaseCheckSettingTableMem where cameraID='%s' and cmosID=%d" % (hvpd[0], hvpd[1]))
        _PhaseCheck = cur.fetchmany(1)[0]
    except Exception, e:
        mylog.error(str(e))
        return
    _xy8_3 = []
    if 0 != _ai_setting[6]: #menual set
        for i in range(24):
            _xy8_3.append(_ai_setting[7+i])
    else:
        if None == _ai_out:
            return
        for i in range(24):
            _xy8_3.append(_ai_out[11+i])

    _dict_msg = {}
    _need_update = 0
    if 0 == hvpd[1]:
        _CmosOffset = 1
    else:
        _CmosOffset = 4
    _vals = [None,None,None]
    for i in range(_ai_setting[3]):
        _vals[i] = calc_phase_val3(_xy8_3[8*i:8*(i+1)])
        if None == _vals[i]:
            mylog.debug("%s space%d All position is 0000"%(hvpd[0], i+1))
            return
        _dict_buff = {"phase%dpos"%(i+_CmosOffset):_vals[i]}
        _dict_msg.update(_dict_buff)

    mylog.debug("%s update phase to %s @ %s" % (hvpd[0], json.dumps(_dict_msg), hvpd[4]))
    (_ret, err)=wtclib.http_get_cgi_msg2device(_dict_msg, hvpd[4], cgi_name="setting")
    if(0 == _ret):
        mylog.warning('update phase to %s %s'%(hvpd[0], err))
        return
    mylog.debug('update phase to %s %s' % (hvpd[0], err))
    try:
        cur.execute("update CameraPhaseCheckSettingTableMem set phase1pos='%s',phase2pos='%s',phase3pos='%s',"
                    "RenewTimet=%d, RenewDate=now() where cameraID='%s' and cmosID=%d"
                    %(_vals[0],_vals[1],_vals[2], int(time.time()),hvpd[0], hvpd[1]))
    except Exception, e:
        mylog.error(str(e))
        return


import hvpd_status
def get_one_hvpd_version(hvpd, cur):
    global mylog
    _timeSec = int(time.time())
    try:
        _a1 = cur.execute("select * from HvpdVersionTableMem where cameraID='%s'"%hvpd[0])
        if 0 != _a1:
            _hvpdVersion = cur.fetchmany(1)[0]
            if _timeSec - _hvpdVersion[6] < 30*60:
                return 0
    except Exception, e:
        mylog.error(str(e))
        return -2

    requrl = "http://"+hvpd[4]+"/cgi-bin/status.cgi"

    dic2 = hvpd_status.get_hvpd_status(requrl)
    if None == dic2:
        mylog.debug("get None version " + requrl)
        return 0

    if not "CAMERA_VERSION" in dic2:
        return 0
    if not "UART_VERSION" in dic2:
        return 0
    if not "UDP_VERSION" in dic2:
        return 0
    if not "HARDVER" in dic2:
        _hard_ver = '0'
    else:
        _hard_ver = dic2['HARDVER']

    try:
        _sql_str = "insert into HvpdVersionTableMem(cameraID, uart_version,camera_version,udp_version,hard_ver, renewtime, renewtimet)values" \
                   "('%s','%s','%s','%s','%s',now(),%d)ON DUPLICATE KEY UPDATE uart_version='%s',camera_version='%s',udp_version='%s'," \
                   "hard_ver='%s',renewtime=now(),renewtimet=%d"\
                   %(hvpd[0], dic2["UART_VERSION"], dic2["CAMERA_VERSION"], dic2["UDP_VERSION"],_hard_ver,_timeSec, dic2["UART_VERSION"],
                     dic2["CAMERA_VERSION"], dic2["UDP_VERSION"], _hard_ver,_timeSec)
        mylog.debug("%s Version:UDP=%s,UART=%s,CAMERA=%s"%(hvpd[0], dic2["UDP_VERSION"], dic2["UART_VERSION"],dic2["CAMERA_VERSION"]))
        cur.execute(_sql_str)
        return 0
    except Exception, e:
        mylog.info(_sql_str)
        mylog.info(str(e))
        return -1

"""only renew the hvpd which is online in 10min"""
def renew_hvpd_phaseCheck_para(cur):
    global mylog
    _sql_str = "select * from OnlineHvpdStatusTableMem where connectTimet>%d"%(int(time.time())-10*60)
    try:
        a1 = cur.execute(_sql_str)
    except Exception, e:
        mylog.error(_sql_str)
        mylog.error(str(e))
        return
    if 0 == a1:
        return
    mylog.debug("renew %d hvpds phaseCheck"%a1)
    try:
        _onlineHvpds = cur.fetchmany(a1)
    except Exception, e:
        mylog.error(_sql_str)
        mylog.error(str(e))
        return
    for _hvpd in _onlineHvpds:
        if 0 != wdi(cur):
            return
        if None == _hvpd[4]:
            continue
        renew_a_hvpd_phaseCheck(_hvpd, cur)
        if 0 != get_one_hvpd_version(_hvpd, cur):
            return

def check_ucmq_MQs(statusUrl, resetUrl, maxLen):
    global mylog
    try:
        res_data = urllib2.urlopen(statusUrl)
        res = res_data.read()
        res_data.close()
        dict_status = json.loads(res)
    except Exception, e:
        mylog.debug(str(e))
        return
    if not "unread" in dict_status:
        return
    if dict_status["unread"] > maxLen:
        try:
            res_data = urllib2.urlopen(resetUrl)
            res = res_data.read()
            res_data.close()
        except Exception, e:
            mylog.debug(str(e))

OFFLINE_SECOND = 15*60
def Set_Offline_camera_space2Used(cur):
    global mylog
    _timeSec = int(time.time())
    try:
        cur.execute("select * from equipment2cameraidmem")
        _equipments = cur.fetchall()
        for _equip in _equipments:
            if None == _equip[4]:   #one side hvpd is not need to force status to using
                continue

            if 0 == cur.execute("select * from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d"%(_equip[2], _equip[3])):
                continue
            _onlineCamera = cur.fetchone()

            if _timeSec - _onlineCamera[10] > OFFLINE_SECOND:
                if 0 == _equip[3]:
                    _offset = 1
                else:
                    _offset = 4
                for i in range(3):
                    cur.execute("update spacestatustable set CarportStatus=1 where CarportStatus=0 and Spaceid='%s%d'"%(_equip[2],i+_offset))


            if 0 != cur.execute("select * from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d"%(_equip[4], _equip[5])):
                _onlineCamera = cur.fetchone()
                if _timeSec - _onlineCamera[10] > OFFLINE_SECOND:
                    if 0 == _equip[5]:
                        _offset = 1
                    else:
                        _offset = 4
                    for i in range(3):
                        cur.execute(
                            "update spacestatustable set CarportStatus=1 where CarportStatus=0 and Spaceid='%s%d'" % (
                            _equip[4], i + _offset))

    except Exception, e:
        mylog.error(str(e))


def update_LampSettingTable_from_aiSetting(cur):
    global mylog
    try:
        _a1 = cur.execute("select * from AiSettingTableMem where user_manual_parking_line=1 and Slot_count<>3")
        mylog.debug("%d hvpd Carport setting is changed"%_a1)
        if 0 == _a1:
            return 0

        _AiSettings = cur.fetchmany(_a1)
        for _AiSetting in _AiSettings:
            if 0 == _AiSetting[3]:
                continue
            if 0 == cur.execute("select * from hvpd2lampsettingtablemem where cameraID='%s' and cmosID=%d"%(_AiSetting[0], _AiSetting[1])):
                continue
            _camera2Equipments = cur.fetchmany(1)[0]
            for i in range(3,6):
                if None == _camera2Equipments[i]:
                    continue
                if 0 == cur.execute("select * from lampsettingtablemem where equipmentID='%s'"%_camera2Equipments[i]):

                    continue
                _LampSetting = cur.fetchmany(1)[0]
                if 0 != _LampSetting[10] or 0 != _LampSetting[11]:#user manual control
                    continue

                if 0 == cur.execute("select * from equipment2cameraidmem where equipmentID='%s'"%_camera2Equipments[i]):
                    continue
                _equipInfo = cur.fetchmany(1)[0]
                _a1 = cur.execute("select * from AiSettingTableMem where cameraID='%s' and cmosID=%d"%(_equipInfo[2], _equipInfo[3]))
                _sql = "update lampsettingtablemem set "

                if 0 == _equipInfo[3]:
                    _cmosOffset = 0
                else:
                    _cmosOffset = 3
                if 0 == _a1:
                    _spaceAll = 3
                    for j in range(1,4):
                        _sql += "Space%dID='%s',"%(j, (_equipInfo[2]+str(_cmosOffset+j)))
                else:
                    _AiSetting0 = cur.fetchmany(1)[0]
                    if 0 == _AiSetting0[3]:
                        continue
                    _spaceAll = _AiSetting0[3]
                    for j in range(_AiSetting0[3]):
                        _sql += "Space%dID='%s',"%(j+1, (_equipInfo[2]+str(_cmosOffset+j+1)))

                if None != _equipInfo[4]:
                    _a1 = cur.execute("select * from aisettingtable where cameraID='%s' and cmosID=%d"
                                      % (_equipInfo[4], _equipInfo[5]))
                    if 0 == _equipInfo[5]:
                        _cmosOffset = 1
                    else:
                        _cmosOffset = 4
                    if 0 == _a1:
                        for j in range(3):
                            _sql += "Space%dID='%s'," % (j+_spaceAll+1, (_equipInfo[4] + str(_cmosOffset + j)))
                        _spaceAll += 3
                    else:
                        _AiSetting1 = cur.fetchmany(1)[0]
                        for j in range(_AiSetting1[3]):
                            _sql += "Space%dID='%s'," % (j+_spaceAll+1, (_equipInfo[4] + str(_cmosOffset + j)))
                        _spaceAll += _AiSetting1[3]
                _timeSec = int(time.time())
                for j in range(_spaceAll+1, 7):
                    _sql += "Space%dID=NULL,"%j
                _sql += "SpaceAll=%d, set_time=now(),set_timet=%d where equipmentID='%s'"%(_spaceAll, _timeSec,_camera2Equipments[i])
                mylog.debug("%s is %d spaces"%(_camera2Equipments[i], _spaceAll))
                cur.execute(_sql)
                cur.execute("update AiSettingTableMem set Event1Flag=1 where cameraID='%s' and cmosID=%d"
                            %(_AiSetting[0], _AiSetting[1]))
                cur.execute("update hvpd2lampsettingtablemem set set_time=now(),set_timet=%d where cameraID='%s' and cmosID=%d"
                            %(_timeSec,_AiSetting[0], _AiSetting[1]))
    except Exception, e:
        mylog.info(str(e))
        return -1
    return 0


def renew_memTables_from_hd(cur):
    global mylog
    _timeSec = int(time.time())
    try:
        a1 = cur.execute("select * from LampSettingTable")
        mylog.debug("renew %d from LampSettingTable"%a1)
        if 0 != a1:
            _tables = cur.fetchmany(a1)
            for _table in _tables:
                #cur.execute("update LampSettingTable set set_timet=%d,set_time=now() where equipmentID='%s'"% (_timeSec,_table[0]))
                if _table[3] > 6 or _table[3] < 1: #not allowed
                    continue
                _ret = -1
                for i in range(_table[3]):
                    if None == _table[4+i]:
                        _ret = 0
                if 0 == _ret:
                    continue

                try:
                    _a2 = cur.execute("select output from %s where Flag_used='xox'" % (_table[2]))
                except:
                    continue

                _sql = "insert into LampSettingTableMem(equipmentID,CtrlTableName, SpaceAll"
                for i in range(1,_table[3]+1):
                    _sql += ",Space%dID"%(i)
                _sql += ", ManualCtrLampFlag, ManualCtrSpaceFlag)values('%s', '%s', %d"%(_table[0], _table[2], _table[3])
                for i in range(_table[3]):
                    if None != _table[i+4]:
                        _sql += ",'%s'"%_table[i+4]
                    else:
                        _sql += ",NULL"
                _sql += ",%d, %d)ON DUPLICATE KEY UPDATE CtrlTableName='%s', SpaceAll=%d"%(_table[10],_table[11],_table[2],_table[3])
                for i in range(_table[3]):
                    _sql += ",Space%dID='%s'"%(i+1,_table[i+4])

                for i in range(_table[3]+1,7):
                    _sql += ",Space%dID=NULL"%(i)

                _sql += ",ManualCtrLampFlag=%d,ManualCtrSpaceFlag=%d,set_time=now()"%(_table[10],_table[11])

                cur.execute(_sql)
    except Exception, e:
        return -1
    try:
        a1 = cur.execute("select * from hvpd2LampSettingTable")
        mylog.debug("renew %d from hvpd2LampSettingTable" % a1)
        if 0 != a1:
            _tables = cur.fetchmany(a1)
            for _table in _tables:
                if None == _table[3] or '' == _table[3]:
                    continue

                _sql = "insert into hvpd2LampSettingTableMem(cameraID, cmosID"
                for i in range(1,4):
                    _sql += ",Effect%dEquipID"%(i)
                _sql += ")values('%s', %d"%(_table[0], _table[1])
                for i in range(3,6):
                    if None != _table[i]:
                        _sql += ",'%s'"%_table[i]
                    else:
                        _sql += ",NULL"
                _sql += ")ON DUPLICATE KEY UPDATE Effect1EquipID='%s'"%_table[3]
                if None != _table[4]:
                    _sql += ",Effect2EquipID='%s'"%_table[4]
                    if None != _table[5]:
                        _sql += ",Effect3EquipID='%s'" % (_table[5])
                    else:
                        _sql += ",Effect3EquipID=NULL"
                else:
                    _sql += ",Effect2EquipID=NULL,Effect3EquipID=NULL"
                _sql += ",set_time=now()"

                cur.execute(_sql)

    except Exception, e:
        return -1
    return 0


def init_lampSettingMem(cur):
    global mylog
    try:
        a1 = cur.execute("select * from lampsettingtable")
        mylog.info("init %d LampSettingMem" % a1)
        if 0 != a1:
            _LampSettings = cur.fetchmany(a1)

            for _Lamp in _LampSettings:
                if _Lamp[3] > 6 or _Lamp[3] < 1:
                    continue

                if 55 == _Lamp[10]:
                    if None == _Lamp[2] or '' == _Lamp[2]:
                        continue
                    if 0 == cur.execute("select * from %s"%_Lamp[2]):
                        continue

                if 0 == _Lamp[10] and 0 == _Lamp[11]:
                    continue

                _sql_str = "insert into lampsettingtablemem(equipmentID,CtrlTableName,SpaceAll," \
                           "ManualCtrLampFlag,ManualCtrSpaceFlag)values('%s','%s',%d,%d,%d)" \
                           "ON DUPLICATE KEY UPDATE CtrlTableName='%s',SpaceAll=%d," \
                           "ManualCtrLampFlag=%d,ManualCtrSpaceFlag=%d"%(_Lamp[0],_Lamp[2],_Lamp[3],_Lamp[10],
                                                                         _Lamp[11],_Lamp[2],_Lamp[3],_Lamp[10],
                                                                         _Lamp[11])
                cur.execute(_sql_str)
                _sql_str = "update lampsettingtablemem set "
                for i in range(_Lamp[3]):
                    if None != _Lamp[i+4]:
                        _sql_str += "Space%dID='%s',"%(i+1,_Lamp[4+i])
                    else:#not all space is set,it is not allowed,so close manual control
                        _sql_str += "ManualCtrSpaceFlag=0,"
                        mylog.error("%s have %d space,%d is NULL"%(_Lamp[0],_Lamp[3], i+1))
                        break
                for i in range(_Lamp[3],6):
                    _sql_str += "Space%dID=NULL,"%(i+1)
                _sql_str += "set_time=now() where equipmentID='%s'"%_Lamp[0]
                cur.execute(_sql_str)
        a1 = cur.execute("select * from hvpd2lampsettingtable")
        if 0 != a1:
            _Hvpd2Lamps = cur.fetchmany(a1)
            for _Hvpd in _Hvpd2Lamps:
                if None == _Hvpd[3]:
                    continue
                _sql_str = "insert into hvpd2lampsettingtablemem(cameraID,cmosID,Effect1EquipID)values('%s',%d,'%s')" \
                           "ON DUPLICATE KEY UPDATE Effect1EquipID='%s'"%(_Hvpd[0],_Hvpd[1],_Hvpd[3],_Hvpd[3])
                cur.execute(_sql_str)
                if None == _Hvpd[4]:
                    continue
                _sql_str = "update hvpd2lampsettingtablemem set Effect2EquipID='%s',"%_Hvpd[4]
                if None != _Hvpd[5]:
                    _sql_str += "Effect3EquipID='%s',"%_Hvpd[5]
                else:
                    _sql_str += "Effect3EquipID=NULL,"
                _sql_str += "set_time=now() where cameraID='%s' and cmosID=%d"%(_Hvpd[0],_Hvpd[1])
                cur.execute(_sql_str)
    except Exception, e:
        print str(e)
        return -1

def renew_memTables2hd():
    global cur
    _tables = cur.fetchmany(cur.execute("select * from LampSettingTableMem where ReNewFlag=2"))
    for _table in _tables:
        try:
            cur.execute("update LampSettingTableMem set ReNewFlag=2 where equipmentID='%s'"%_table[0])
            if 0 == cur.execute("select * from LampSettingTable where equipmentID='%s'"%_table[0]):
                cur.execute("insert into LampSettingTable from select * from LampSettingTableMem where equipmentID='%s'"%_table[0])

        except:
            pass
    _tables = cur.fetchmany(cur.execute("select * from hvpd2LampSettingTableMem where ReNewFlag=2"))
    for _table in _tables:
        try:
            cur.execute("update hvpd2LampSettingTableMem set ReNewFlag=0 "
                        "where cameraID='%s'and cmosID=%d" % (_table[0], _table[1]))
            if 0 == cur.execute("select * from hvpd2LampSettingTable "
                                "where cameraID='%s' and cmosID=%d"%(_table[0], _table[1])):
                cur.execute("insert into hvpd2LampSettingTable from select * from hvpd2LampSettingTableMem "
                            "where cameraID='%s' and cmosID=%d"%(_table[0], _table[1]))

        except:
            pass

def config_video_fmt():
    global cur,mylog

    try:
        _a1 = cur.execute("select * from video_user_set where video_timet != 0")
        mylog.info("config_video_fmt %d hvpds" % _a1)
        if 0 == _a1:
            return

        _tables = cur.fetchall()
    except Exception,e:
        mylog.error(str(e))
        return

    for _hvpd in _tables:
        try:
            _sql = "select * from onlinehvpdstatustablemem where cameraID='%s' and cmosID=%d"%(_hvpd[0],_hvpd[1])
            if 0 == cur.execute(_sql):
                continue
            _online = cur.fetchone()
            if 0 == _hvpd[4]:
                _dict_msg = {"Fvideo_en":"0"}
            else:
                _dict_msg = {"Fvideo_en":"1","Fvideo_def":"%d"%_hvpd[5],"Fvideo_bitrate":"%d"%_hvpd[6]}


            _ret, err = wtclib.http_get_cgi_msg2device(_dict_msg, _online[4], "setting")
            if 1 == _ret:
                cur.execute("update video_user_set set video_timet=0,set_time=now() where cameraID='%s' and cmosID=%d" % (
                _hvpd[0], _hvpd[1]))
                mylog.info("%s video fmt update is OK @ %s"%(_hvpd[0], _online[4]))
            else:
                mylog.warning("config_video_fmt "+"http_get_cgi_msg2device "+err)
                mylog.warning("hvpd ip %s"%_online[4])

        except Exception,e:
            mylog.error(str(e))
            mylog.error(_sql)

    return

def insert_bay_using_log(cur, loc_time):
    global mylog
    try:
        if 0 == loc_time.tm_hour:
            #localtime1 = time.localtime(time.time()-22*3600)
            cur.execute("delete from bay_using_log where day=%d"%loc_time.tm_mday)
        _sql_str = "select sum(parking1State+parking2State+parking3State) from aiouttable"
        if 0 != cur.execute(_sql_str):
            _using, = cur.fetchone()
            _sql_str = "insert into bay_using_log(day,hour,used_bays)values(%d,%d,%d)ON DUPLICATE KEY " \
                       "UPDATE used_bays=%d"%(loc_time.tm_mday,loc_time.tm_hour,_using,_using)
            cur.execute(_sql_str)
            mylog.info("bays using %d"%_using)
            return 0
        return -2
    except Exception,e:
        mylog.error(str(e))
        return -1

if __name__ == '__main__':
    if not os.path.isdir("../log/configfiles/"):
        try:
            os.mkdir("../log/configfiles/")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylog = wtclib.create_logging("../log/configfiles/configfiles.log")
    mylog.info("start")

    url_ret, userjpgMQ_status_url = wtclib.get_ucmq_status_url("userjpg")
    if 0 == url_ret:
        userjpgMQ_status_url = "http://127.0.0.1:8803/?opt=status_json&ver=2&name=userjpg"
    url_ret, userjpgMQ_reset_url = wtclib.get_ucmq_reset_url("userjpg")
    if 0 == url_ret:
        userjpgMQ_reset_url = "http://127.0.0.1:8803/?opt=reset&ver=2&name=userjpg"
    url_ret, downloadMQ_status_url = wtclib.get_ucmq_status_url("downloadmq")
    if 0 == url_ret:
        downloadMQ_status_url = "http://127.0.0.1:8803/?opt=status_json&ver=2&name=downloadmq"
    url_ret, downloadMQ_reset_url = wtclib.get_ucmq_reset_url("downloadmq")
    if 0 == url_ret:
        downloadMQ_reset_url = "http://127.0.0.1:8803/?opt=reset&ver=2&name=downloadmq"

    _ConfChangeTime = os.stat("../conf/").st_ctime
    while True:
        (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)

    renew_config_info_sql(cur, 0)
    _ConfDelay = 2
    _pid = os.getpid()
    _timeSecInt = int(time.time())
    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 300, %d,'%s')" % (_pid, __file__, _timeSecInt,ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "configfiles" in _dic1:
            _version = _dic1["configfiles"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('configfiles','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylog.error(str(e) + time.asctime())

    _min10_delay_cnt = 2
    socket.setdefaulttimeout(3)
    check_ucmq_MQs(userjpgMQ_status_url, userjpgMQ_reset_url, 1000)
    check_ucmq_MQs(downloadMQ_status_url, downloadMQ_reset_url, 1000)

    init_lampSettingMem(cur)
    localtime1 = time.localtime()
    _using_log_hour = localtime1.tm_hour
    while True:
        localtime1 = time.localtime()
        if _using_log_hour != localtime1.tm_hour:
            if 0 == insert_bay_using_log(cur, localtime1):
                _using_log_hour = localtime1.tm_hour

        if 0 != wdi(cur):
            (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
            if None == cur:
                mylog.error(err)
            time.sleep(2)
            continue

        """ Auto renew Config ini files, delay 20times, near 60sec"""
        _ConfTime = os.stat("../conf/").st_ctime
        if _ConfChangeTime != _ConfTime:
            _ConfDelay -= 1
            if _ConfDelay <= 0:
                renew_config_info_sql(cur, _ConfChangeTime)
                _ConfChangeTime = os.stat("../conf/").st_ctime
                _ConfDelay = 10

        _min10_delay_cnt -= 1
        if 0 == _min10_delay_cnt:
            _min10_delay_cnt =50
            check_ucmq_MQs(userjpgMQ_status_url, userjpgMQ_reset_url, 1000)
            check_ucmq_MQs(downloadMQ_status_url, downloadMQ_reset_url, 1000)
            renew_hvpd_phaseCheck_para(cur)
            #Set_Offline_camera_space2Used(cur)
            #init_lampSettingMem(cur)

        fix_hvpd_ip_addr(cur)
        check_and_upgrade_hvpd(cur)
        check_and_upgrade_fixip_hvpd(cur)

        update_LampSettingTable_from_aiSetting(cur)
        renew_memTables_from_hd(cur)
        config_video_fmt()
        mylog.debug("alive @ "+time.asctime())
        time.sleep(6)