import wtclib
import os, time, sys
import socket
import threading
import ConfigParser
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
        cnt = 0
        cur.execute("update Space2LedTable set RegionSn=-10")#-10 means not use
        #if the bay is not config to a LED displayer, the RegionSn is 0, no LED displayer Region is 0,so,
        #the 0 region will not be showed in LED
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')

                _sql = "insert into Space2LedTable(cameraID,bay,RegionSn) values('%s',%s, %s)ON DUPLICATE KEY UPDATE " \
                       "RegionSn=%s" % (list1[1], list1[2], list1[0], list1[0])
                cur.execute(_sql)
                cnt += 1
            else:
                break
    except Exception, e:
        mylog.error(str(e))
    finally:
        filei.close()
        print "insert %d"%cnt
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
        cur.execute("update SpaceStatusTable set CarportStatus=0 where CarportStatus=2")
        #for new configuration, clear the Old
        while True:
            line = filei.readline()

            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("update SpaceStatusTable set CarportStatus=2 where cameraID='%s' and bay=%s"%(list1[0],list1[1]))
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


def renew_screen_config_info_sql(cur, reNewTime):
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
    global mylog,sqlite3_cur
    mylog.debug("fix hvpd ip")
    try:
        a1 = cur.execute("select * from camera_ipaddrsettingtable where ReNewFlag<>0")
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
            if 2 == _hvpdIP[1]:
                a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'" % (_hvpdIP[0]))
                if 0 == a1:
                    continue
                _OnlineInfo = cur.fetchmany(1)[0]
                _dic1 = {"Fip": "0", "Fmask": "0", "Frouter": "0", "Fip_set": 0}
                _timeSec = time.time()
                wdi(cur)
                (val, err) = wtclib.http_get_cgi_msg2device(_dic1, ip=_OnlineInfo[4], cgi_name="setting")
                if 0 != val:
                    cur.execute("update camera_ipaddrsettingtable set ReNewFlag=0, NewIP=NULL,NewMask=NULL,"
                                "NewGateway=NULL where cameraID='%s'" % (_hvpdIP[0]))
                continue

            val = 0
            err = "IP Error "
            if None == _hvpdIP[5]:
                val = 3
                err += "ip=None "
            if None == _hvpdIP[6]:
                val = 4
                err += "mask=None "
            if None == _hvpdIP[7]:
                val = 5
                err += "router=None"
            if 0 == val:
                err = ""
            if 0 == val and 0 == check_ip_is_ok(_hvpdIP[5]) and 0 == check_ip_is_ok(_hvpdIP[6]) and 0 == check_ip_is_ok(_hvpdIP[7]):
                a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'"%(_hvpdIP[0]))
                if 0 == a1:
                    continue
                _OnlineInfo = cur.fetchmany(1)[0]
                _dic1 = {"Fip":_hvpdIP[5], "Fmask":_hvpdIP[6], "Frouter":_hvpdIP[7], "reboot":1,"Fip_set":1}
                _timeSec = time.time()
                wdi(cur)
                (val, err) = wtclib.http_get_cgi_msg2device(_dic1, ip=_OnlineInfo[4], cgi_name="setting")

            else:
                val = 2
                err = "IP is not good where ip=%s mask=%s router=%s" % (_hvpdIP[5], _hvpdIP[6], _hvpdIP[7])

            if 0 != val:
                cur.execute("update camera_ipaddrsettingtable set ReNewFlag=0 where  cameraID='%s'"%(_hvpdIP[0]))
                #print "fix %s ip to %s,%s,%s"%(_hvpdIP[0], _hvpdIP[6], _hvpdIP[7], _hvpdIP[8])
                mylog.info("fix %s ip to %s,%s,%s"%(_hvpdIP[0], _hvpdIP[5], _hvpdIP[6], _hvpdIP[7]))

            if "" != err:
                mylog.warning(err)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylog.error(str(e))


def check_and_upgrade_hvpd(cur):
    global mylog,sqlite3_cur
    try:
        a1 = cur.execute("select * from camera_upgradetable where ReNewFlag<>0")
        if 0 == a1:
            mylog.debug("0 hvpd need upgrade firmware")
            return
        mylog.info("%d hvpds need to upgrade firmware"%a1)
        _pid = os.getpid()
        _hvpds = cur.fetchmany(a1)
        for _hvpd in _hvpds:
            if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'and cmosID=0"%(_hvpd[0])):
                continue
            _camera = cur.fetchmany(1)[0]
            _timeSec = time.time()
            if _timeSec - _camera[10] > 10*60:
                mylog.debug("%s is timeout, last connect time is %s"%(_camera[0],_camera[9]))
                continue
            wdi(cur)
            mylog.info(_hvpd[0]+" upgrade firmware "+_hvpd[1])
            ret = wtclib.http_post_file2device("../../firmwares/" + _hvpd[1], _camera[4], "upgrade.cgi")
            if 200 == ret:
                cur.execute("update camera_upgradetable set ReNewFlag=0, end_time=now() where cameraID='%s' and cmosID=0"%_hvpd[0])
                cur.execute("update camera_versiontablemem set renewtimet=0 where cameraID='%s'"%_hvpd[0])

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

"""renew data in every 30mins"""
def renew_a_hvpd_phaseCheck(hvpd, cur):
    global mylog

    try:
        if 0 == cur.execute("select * from aisettingtable_camera_mem where user_manual_parking_line=1 and "
                            "cameraID='%s' and cmosID=%d"%(hvpd[0], hvpd[1])):
            mylog.info("%s is not manual parking line"%hvpd[0])
            return
        _aisettings = cur.fetchone()
        _bays = _aisettings[2]
        if _bays > 3 or 4 == _aisettings[3]:
            _bays = 2
        cur.execute("select * from spacestatustable where cameraID='%s' and cmosID=%d" % (hvpd[0], hvpd[1]))
        _PhaseCheck = cur.fetchall()
    except Exception, e:
        mylog.error(str(e))
        return

    _dict_msg = {}
    _need_update = 0
    if 0 == hvpd[1]:
        _CmosOffset = 1
    else:
        _CmosOffset = 200

    for i in range(_bays):
        _vals = calc_phase_val2(_aisettings[6+8*i:6+8*(i+1)])
        if None == _vals:
            mylog.debug("%s space%d All position is 0000"%(hvpd[0], i+1))
            return
        _dict_buff = {"phase%dpos"%(i+_CmosOffset):_vals}
        _dict_msg.update(_dict_buff)
        if _vals != _PhaseCheck[i][16]:

            try:
                cur.execute("update spacestatustable set phase_pos='%s',"
                            "phase_Timet=%d, phase_Date=now() where cameraID='%s' and cmosID=%d and bay=%d"
                            % (_vals,int(time.time()), hvpd[0], hvpd[1],i+1))
            except Exception, e:
                mylog.error(str(e))
                return


    mylog.debug("%s update phase to %s @ %s" % (hvpd[0], json.dumps(_dict_msg), hvpd[4]))
    (_ret, err)=wtclib.http_get_cgi_msg2device(_dict_msg, hvpd[4], cgi_name="setting")
    if(0 == _ret):
        return

    else:
        mylog.debug("%s update phase next time"%hvpd[0])

import hvpd_status
def get_one_hvpd_version(hvpd, cur):
    global mylog
    _timeSec = int(time.time())
    try:
        _a1 = cur.execute("select * from camera_versiontablemem where cameraID='%s'"%hvpd[0])
        if 0 != _a1:
            _hvpdVersion = cur.fetchone()
            if _timeSec - _hvpdVersion[8] < 30*60:
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
        _sql_str = "insert into camera_versiontablemem(cameraID, uart_version,camera_version,udp_version,hard_ver, renewtime, renewtimet)values" \
                   "('%s','%s','%s','%s','%s',now(),%d)ON DUPLICATE KEY UPDATE uart_version='%s',camera_version='%s',udp_version='%s'," \
                   "hard_ver='%s',renewtime=now(),renewtimet=%d"\
                   %(hvpd[0], dic2["UART_VERSION"], dic2["CAMERA_VERSION"], dic2["UDP_VERSION"],_hard_ver,_timeSec, dic2["UART_VERSION"],
                     dic2["CAMERA_VERSION"], dic2["UDP_VERSION"], _hard_ver, _timeSec)
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

def Load_aisetting_from_hd(_cur, time_set):
    global mylog
    #_timeSecInt = int(time.time())
    try:
        _sql = "select * from aisettingtable_camera"
        if 0 != time_set[0]:
            _sql += " where set_time > '%s'"%time_set[0]
            _datetime_camera = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            _day1 = datetime.datetime.now()-datetime.timedelta(days=1)
            _datetime_camera = _day1.strftime("%Y-%m-%d %H:%M:%S")
        _a1 = _cur.execute(_sql)

        mylog.info("load %d new AI camera setting from HD" % _a1)
        if 0 != _a1:
            _cameras = _cur.fetchall()
            if None != _cameras:
                _camera_time = []
                for _camera in _cameras:
                    _camera_time.append(_camera[30])
                    if 0 == _cur.execute("select * from aisettingtable_camera_mem where cameraID='%s'"%_camera[0]):
                        _cur.execute("insert into aisettingtable_camera_mem(cameraID)values('%s')"%_camera[0])
                    _sql = "replace into aisettingtable_camera_mem select * from aisettingtable_camera where cameraID='%s'"%(_camera[0])
                    _cur.execute(_sql)
                    for i in range(_camera[2]):
                        if 0 == _cur.execute("select * from spacestatustable where cameraID='%s' and bay=%d"%(_camera[0], i+1)):
                            _cur.execute("insert into spacestatustable(cameraID,bay)values('%s',%d)"%(_camera[0], i+1))
                        if 0 == _cur.execute("select * from aisettingtable_bay_mem where cameraID='%s' and bay=%d"%(_camera[0], i+1)):
                            _cur.execute("insert into aisettingtable_bay_mem(cameraID,bay)values('%s',%d)"%(_camera[0], i+1))
                    _sql_str = "delete from spacestatustable where cameraID='%s' and bay>%d"%(_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    mylog.info(_sql_str)
                    _sql_str = "delete from aisettingtable_bay_mem where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    mylog.info(_sql_str)
                    _sql_str = "delete from aiouttable_bay where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    _sql_str = "delete from aiouttable_bay2 where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    _sql_str = "delete from reouttable_bay where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    _sql_str = "delete from reoutfiltertable where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                    _sql_str = "delete from refiltertable where cameraID='%s' and bay>%d" % (_camera[0], _camera[2])
                    _cur.execute(_sql_str)
                _datetime_camera = max(_camera_time)
    except Exception,e:
        mylog.error(str(e))
        mylog.error(_sql)
    try:
        _sql = "select * from aisettingtable_bay"
        if 0 != time_set[1]:
            _sql += " where set_timet >'%s'"%time_set[1]
            _datetime_bay = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            _day1 = datetime.datetime.now() - datetime.timedelta(days=1)
            _datetime_bay = _day1.strftime("%Y-%m-%d %H:%M:%S")
        _a1 = _cur.execute(_sql)
        mylog.info("load %d new AI camera bay setting from HD" % _a1)
        if 0 == _a1:
            return  [_datetime_camera, _datetime_bay]
        _cameras = cur.fetchall()
        if None != _cameras:
            _camera_time = []
            for _camera in _cameras:
                _camera_time.append(_camera[12])
                _sql = "replace into aisettingtable_bay_mem select * from aisettingtable_bay where cameraID='%s' and bay=%d"\
                       %(_camera[0],_camera[2])
                _cur.execute(_sql)
                mylog.info(_sql_str)
            _datetime_bay = max(_camera_time)
    except Exception,e:
        mylog.error(str(e))
        mylog.error(_sql)
    return _datetime_camera, _datetime_bay


def Load_lamp_setting_from_hd(_cur, set_time):
    global mylog
    _timeSecInt = int(time.time())
    try:
        _sql = "select * from lampsettingtable"
        if 0 != set_time:
            _sql += " where set_timet>%d"%set_time
        _a1 = _cur.execute(_sql)
        mylog.info("load %d new Lamp setting from HD" % _a1)
        if 0 != _a1:
            _lamps = _cur.fetchall()
            for _lamp in _lamps:
                _sql = "insert into lampsettingtablemem(equipmentID,CtrlTableName,lamp_colcor,colcor_name," \
                       "ManualCtrLampFlag,ManualCtrSpaceFlag)values('%s','%s',%d,'%s',%d,%d)ON DUPLICATE KEY UPDATE " \
                       "CtrlTableName='%s',lamp_colcor=%d,colcor_name='%s',ManualCtrLampFlag=%d,ManualCtrSpaceFlag=%d"\
                       %(_lamp[0],_lamp[1],_lamp[2],_lamp[3],_lamp[4],_lamp[5],_lamp[1],_lamp[2],_lamp[3],_lamp[4],_lamp[5])
                _cur.execute(_sql)
                _cur.execute("update lampsettingtable set set_timet=%d"%_timeSecInt)
    except Exception,e:
        mylog.error(str(e))
        mylog.error(_sql)
    return _timeSecInt



if __name__ == '__main__':
    if not os.path.isdir("../log/configfiles/"):
        try:
            os.mkdir("../log/configfiles/")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylog = wtclib.create_logging("../log/configfiles/configfiles.log")
    mylog.info("start")
    _ConfChangeTime = os.stat("../conf/").st_ctime
    while True:
        (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf", "hvpd3db2")
        if None != cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    del err


    _timeSecInt = int(time.time())

    _ConfDelay = 2
    _pid = os.getpid()
    ServerID = wtclib.get_serverID()
    #sqlite3_cur, sqlite3_conn = wtclib.get_a_sqlite3_cur_forever(mylog, "/tmp/softdog.db")
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 300, %d,'%s')" % (_pid, __file__, _timeSecInt,ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "configfiles" in _dic1:
            _version = _dic1["configfiles"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
            del stat
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('configfiles','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
        del _dic1, _version, _pid
    except Exception, e:
        mylog.error(str(e) + time.asctime())
    _min10_delay_cnt = 2
    socket.setdefaulttimeout(3)

    _ip = wtclib.get_ip_addr1("eth0")
    url_ret, userjpgMQ_status_url = wtclib.get_ucmq_status_url("userjpg")
    if 0 == url_ret:
        userjpgMQ_status_url = "http://%s:8803/?opt=status_json&ver=2&name=userjpg" % _ip
    url_ret, userjpgMQ_reset_url = wtclib.get_ucmq_reset_url("userjpg")
    if 0 == url_ret:
        userjpgMQ_reset_url = "http://%s:8803/?opt=reset&ver=2&name=userjpg" % _ip
    url_ret, downloadMQ_status_url = wtclib.get_ucmq_status_url("downloadmq")
    if 0 == url_ret:
        downloadMQ_status_url = "http://%s:8803/?opt=status_json&ver=2&name=downloadmq" % _ip
    url_ret, downloadMQ_reset_url = wtclib.get_ucmq_reset_url("downloadmq")
    if 0 == url_ret:
        downloadMQ_reset_url = "http://%s:8803/?opt=reset&ver=2&name=downloadmq" % _ip

    #check_ucmq_MQs(userjpgMQ_status_url, userjpgMQ_reset_url, 1000)
    check_ucmq_MQs(downloadMQ_status_url, downloadMQ_reset_url, 1000)
    del url_ret

    _aisetting_datetime = Load_aisetting_from_hd(cur, (0,0))
    _lampsetting_timet = Load_lamp_setting_from_hd(cur, 0)
    renew_screen_config_info_sql(cur, 0)
    while True:

        if 0 != wdi(cur):
            (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf", "hvpd3db2")
            if None == cur:
                mylog.error(err)
            time.sleep(2)
            continue

        """ Auto renew Config ini files, delay 20times, near 60sec"""
        _ConfTime = os.stat("../conf/").st_ctime
        if _ConfChangeTime != _ConfTime:
            _ConfDelay -= 1
            if _ConfDelay <= 0:
                renew_screen_config_info_sql(cur, _ConfChangeTime)
                _ConfChangeTime = os.stat("../conf/").st_ctime
                _ConfDelay = 10

        _min10_delay_cnt -= 1
        if 0 == _min10_delay_cnt:
            _min10_delay_cnt =50
            #check_ucmq_MQs(userjpgMQ_status_url, userjpgMQ_reset_url, 1000)
            check_ucmq_MQs(downloadMQ_status_url, downloadMQ_reset_url, 1000)
            renew_hvpd_phaseCheck_para(cur)


        fix_hvpd_ip_addr(cur)
        check_and_upgrade_hvpd(cur)
        _aisetting_datetime = Load_aisetting_from_hd(cur, _aisetting_datetime)
        _lampsetting_timet = Load_lamp_setting_from_hd(cur, _lampsetting_timet)

        config_video_fmt()
        mylog.debug("alive @ "+time.asctime())
        time.sleep(6)