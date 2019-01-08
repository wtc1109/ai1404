import bin.wtclib
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
    filei = open(path, 'r')
    try:

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
            else:
                break
    finally:
        filei.close()
    return



def update_screen_config(path, cur):
    filei = open(path, 'r')
    try:

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
                            "Action=%s, Font=%s, Color=%s, Display=%s"% (_region[0], _region[1], _region[2], _region[3], _region[4], _region[5], _region[6],
                                  _region[7], _region[8], _region[0], _region[1], _region[2], _region[3], _region[4],
                                  _region[5], _region[6],_region[7] ))
            else:
                break
    finally:
        filei.close()
    return

def update_screen2_config(path, cur):
    filei = open(path, 'r')
    try:

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
                    _region = list1[6+i].split(',')
                    cur.execute("update ScreenConfigTable set Region%d = %s"
                                " where ScreenSn='%s'"
                                "" % (i+1, _region[8], list1[0]))
                for _RegionInfo in list1[6:]:
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
            else:
                break
    finally:
        filei.close()
    return


def update_region_config(path, cur):
    filei = open(path, 'r')
    try:

        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, CarportStatus) "
                            "values('%s', '%s', 0)ON DUPLICATE KEY UPDATE cameraID='%s'"
                            % (list1[1]+list1[2], list1[1],  list1[1]))
                cur.execute("insert into Space2LedTable(Spaceid, RegionSn) "
                            "values('%s', %s)"
                            % (list1[1] + list1[2], list1[0]))
            else:
                break
    finally:
        filei.close()
    return


def update_reserved_parking(path, cur):
    filei = open(path, 'r')
    try:
        cur.execute("update SpaceStatusTable set CarportStatus=0 where CarportStatus=2")
        while True:
            line = filei.readline()

            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("update SpaceStatusTable set CarportStatus=2 where Spaceid='%s'"%(list1[0]+list1[1]))
            else:
                break
    finally:
        filei.close()
    return

def renew_config_info_sql(cur, reNewTime):
    path = "../conf/"
    while not os.path.isdir(path):
        time.sleep(120)
    (snpath, dirs, filenames), = os.walk(path)
    print snpath
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
        if 0 == files.find("HVCS_screen_config"):
            update_screen_config(path+files, cur)
            continue
        if 0 == files.find("HVCS_screen2_config"):
            update_screen2_config(path+files, cur)
            continue
        if 0 == files.find("HVCS_reserved_parking"):
            update_reserved_parking(path+files, cur)
            continue
    return


def fix_hvpd_ip_addr(cur):
    a1 = cur.execute("select * from hvpdIpAddrSettingTable where ReNewFlag<>0")
    if 0 == a1:
        return
    try:
        _hvpds = cur.fetchmany(a1)
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        return
    _pid = os.getpid()

    for _hvpdIP in _hvpds:
        try:

            a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%(_hvpdIP[0], _hvpdIP[1]))
            if 0 == a1:
                continue

            _OnlineInfo = cur.fetchmany(1)[0]
            _dic1 = {"Fip":_hvpdIP[6], "Fmask":_hvpdIP[7], "Frouter":_hvpdIP[8], "reboot":1,"Fip_set":1}

            _timeSec = time.time()
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
            (val, err) = bin.wtclib.http_get_cgi_msg2device(_dic1, ip=_OnlineInfo[4], cgi_name="setting")
            if 1 == val:
                cur.execute("update hvpdIpAddrSettingTable set ReNewFlag=0 where  cameraID='%s' and cmosID=%d"%(_hvpdIP[0], _hvpdIP[1]))
            else:
                print err + " in line: " + str(sys._getframe().f_lineno)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)


def check_and_upgrad_hvpd(cur):
    global mylog
    try:
        a1 = cur.execute("select * from HvpdUpgradeTable where ReNewFlag<>0")
        if 0 == a1:
            return
        _pid = os.getpid()
        _hvpds = cur.fetchmany(a1)
        for _hvpd in _hvpds:
            if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'and cmosID=0"%(_hvpd[0])):
                continue
            _camera = cur.fetchmany(1)[0]
            _timeSec = time.time()
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
            mylog.debug(_hvpd[0]+" upgrade firmware "+_hvpd[2])
            ret = bin.wtclib.http_post_file2device("/home/bluecard/hvpd/firmwares/" + _hvpd[2], _camera[4], "upgrade.cgi")
            if 200 == ret:
                cur.execute("update HvpdUpgradeTable set ReNewFlag=0, end_time=now()")
            time.sleep(0.5)
    except:
        pass


def wdi(cur):
    global mylog
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (int(time.time()), os.getpid()))
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

"""renew data in every 30mins"""
def renew_a_hvpd_phaseCheck(hvpd, cur):
    global mylog
    try:
        a1 = cur.execute("select * from AiSettingTableMem where cameraID='%s' and cmosID=%d"%(hvpd[0], hvpd[1]))
        if (0 == a1):
            return
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
        _vals[i] = calc_phase_val(_xy8_3[8*i:8*(i+1)])
        _dict_buff = {"phase%dpos"%(i+_CmosOffset):_vals[i]}
        _dict_msg.update(_dict_buff)
        if _vals[i] != _PhaseCheck[i+2]:
            _need_update = 1
    _timeSec = int(time.time())
    if _timeSec - _PhaseCheck[5] > 1:#30*60:
        _need_update = 1
    mylog.debug("%s %d update phase to %s @ %s"%(hvpd[0], hvpd[1], json.dumps(_dict_msg), hvpd[4]))
    if 0 != _need_update:
        (_ret, err)= bin.wtclib.http_get_cgi_msg2device(_dict_msg, hvpd[4], cgi_name="setting")
        if(0 == _ret):
            return
        try:
            cur.execute("update CameraPhaseCheckSettingTableMem set phase1pos='%s',phase2pos='%s',phase3pos='%s',"
                        "RenewTimet=%d where cameraID='%s' and cmosID=%d"
                        %(_vals[0],_vals[1],_vals[2], int(time.time()),hvpd[0], hvpd[1]))
        except Exception, e:
            mylog.error(str(e))
            return


data_link = []
tr_start = False
"""usr get method to get a ucmq msg from server"""
class MyHtmlParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global tr_start, data_link
        #print "<%s>"%tag
        if 'tr' == tag and tr_start == False:
            tr_start = True
        if 'input' == tag and True == tr_start:
            dic_val = dict(attrs)
            try:
                val = dic_val["value"]
                data_link.append(val)
            except:
                pass
    def handle_endtag(self, tag):
        global tr_start
        #print "</%s>"%tag
        if 'tr' == tag:
            tr_start = False

    def handle_startendtag(self, tag, attrs):
        #print "<%s/>"%tag
        pass
    def handle_data(self, tag):
        global tr_start
        #print "data=", tag
        if True == tr_start:
            data_link.append(tag)

def get_one_hvpd_version(hvpd, cur):
    global mylog
    requrl = "http://"+hvpd[4]+"/cgi-bin/status.cgi"
    try:
        socket.setdefaulttimeout(1)
        res_data = urllib2.urlopen(requrl)
        res = res_data.read()
        #print res
        res_data.close()
        urllib.urlcleanup()
    except Exception, e:
        mylog.debug(str(e))
        return 0
    parser = MyHtmlParser()
    parser.feed(res)
    #print parser
    #print data_link
    dic2 = {}
    for i in range(len(data_link) / 2):
        msg = data_link[2 * i].strip(' ')
        msg = msg.strip('\r')
        msg = msg.strip('\n')
        if '' == msg:
            continue
            #    print r'%x'%msg
        dic = {data_link[2 * i]: data_link[2 * i + 1]}
        dic2.update(dic)
    #print dic2
    if not "CAMERA_VERSION" in dic2:
        return 0
    if not "UART_VERSION" in dic2:
        return 0
    if not "UDP_VERSION" in dic2:
        return 0
    try:
        _sql_str = "insert into HvpdVersionTableMem(cameraID, uart_version,camera_version,udp_version)values" \
                   "('%s','%s','%s','%s')ON DUPLICATE KEY UPDATE uart_version='%s',camera_version='%s',udp_version='%s'" \
                   ""%(hvpd[0], dic2["UART_VERSION"], dic2["CAMERA_VERSION"], dic2["UDP_VERSION"], dic2["UART_VERSION"],
                       dic2["CAMERA_VERSION"], dic2["UDP_VERSION"])

        cur.execute(_sql_str)
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
        renew_a_hvpd_phaseCheck(_hvpd, cur)
        if 0 != get_one_hvpd_version(_hvpd, cur):
            return




if __name__ == '__main__':
    if not os.path.isdir("../log/"):
        try:
            os.mkdir("../log/")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylog = bin.wtclib.create_logging("../log/configfiles.log")
    mylog.info("start")
    _ConfChangeTime = os.stat("../conf/").st_ctime
    while True:
        (cur, err) = bin.wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)

    renew_config_info_sql(cur, 0)
    _ConfDelay = 2
    _pid = os.getpid()
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 300, %d)" % (_pid, __file__, int(time.time())))
        stat = os.stat(__file__)
        _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('configfiles','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylog.error(str(e) + time.asctime())
    _min10_delay_cnt = 2
    socket.setdefaulttimeout(3)
    while True:
        _timeSec = time.time()
        if 0 != wdi(cur):
            (cur, err) = bin.wtclib.get_a_sql_cur("../conf/conf.conf")
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
            _min10_delay_cnt =100
            fix_hvpd_ip_addr(cur)
            check_and_upgrad_hvpd(cur)
            renew_hvpd_phaseCheck_para(cur)
        mylog.debug("alive @ "+time.asctime())
        time.sleep(6)