import ConfigParser
import Queue
import json
import os
import socket
import sys
import threading
import time, datetime
import fcntl, struct
import wtclib

THREAD_NUM = 3 #how many threads
gQueues = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)


def analyze_udp_info2dict(msg):
    ret = msg.find('LEDID')
    if 0 != ret:
        return None
    #msg.rstrip("\r\n")
    ret = msg.find(':')
    msg2 = msg[ret+1:].rstrip("\r\n")
    list1 =msg2.split(' ')
    return list1

def make_sql_udp_info_str(info, Errflag):
    val = "'%s'," % info[0]
    for i in range(1, 4):
        val += "%s, " % info[i]
    for i in range(4, 11):
        val += "'%s', " % info[i]
    val += info[11] + ','
    for i in range(12, 16):
        val += "'%s', " % info[i]
    val += "%d, %d, " % (info[16], Errflag)

    str1 = "(LEDID , width, height, unitSum, distanceP2P, color, definition, minPix, productName, " \
           "HardwareVersion, softwareVersion, currentSerialNo, MAC, refresh, systemFlag, IPaddress," \
                       "port, ErrorFlag, time) " \
           "values(" + val + " now())"
    return str1

def sql_insert_into_table(UserLog, info, table, cur, Errflag):

    str1 = "insert into "+ table + make_sql_udp_info_str(info, Errflag)
    try:
        cur.execute(str1)
    except Exception, e:
        UserLog.error(str1)
        UserLog.error(str(e))
        return -1
    return 0
def sql_replace_into_table(UserLog, info, table, cur):
    str1 = "replace into "+ table + make_sql_udp_info_str(info) + "where LEDID='%s'"%info[0]
    try:
        cur.execute(str1)
    except Exception, e:
        UserLog.error(str1)
        UserLog.error(str(e))
    return
def update_udp_into2sql(UserLog, info, cur):
    if "00006899999" == info[0]:
        return sql_insert_into_table(UserLog, info, "LedDisplayerUdpErrorInfo", cur)
    try:
        a1 = cur.execute("select * from LedDisplayerUdpInfo where LEDID='" + info[0] + "'")
        if a1 > 1:
            many_prodc = cur.fetchmany(a1)
            for prod in many_prodc:
                cur.execute("insert into LedDisplayerUdpErrorInfo select * from LedDisplayerUdpInfo where id=%d"%prod[0])
                #cur.execute("delete from LedDisplayerUdpInfo where id=%d"%prod[0])
            return 0
    except Exception, e:
        UserLog.error(str(e))
        return -1

    if 0 == a1:
        try:
            a1 = cur.execute("select * from LedDisplayerUdpInfo where MAC='" + info[12] + "'")
            if 0 == a1:
                _ret = sql_insert_into_table(UserLog, info, "LedDisplayerUdpInfo", cur, 0)
                if 0 != _ret:
                    return -1
            else:
                many_prodc = cur.fetchmany(a1)
                for prod in many_prodc:
                    cur.execute(
                        "insert into LedDisplayerUdpErrorInfo select * from LedDisplayerUdpInfo where id=%d" % prod[0])
                _ret = sql_insert_into_table(UserLog, info, "LedDisplayerUdpErrorInfo", cur, 1)
                if 0!= _ret:
                    return -1
        except Exception, e:
            UserLog.error(str(e))
            return -1
    else:
        try:
            a1 = cur.execute("select * from LedDisplayerUdpInfo where MAC='%s'"%info[12])
            if 0 == a1:#different MAC, so error
                _ret = sql_insert_into_table(UserLog, info, "LedDisplayerUdpInfo", cur, 1)
                if 0 != _ret:
                    return -1
            else:
                cur.execute("delete from LedDisplayerUdpInfo where LEDID='%s'"%info[0])
                _ret = sql_insert_into_table(UserLog, info, "LedDisplayerUdpInfo", cur, 0)
                if 0 != _ret:
                    return -1
        except Exception, e:
            UserLog.error(str(e))
            return -1
    return 0


def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), \
                                        0x8915, \
                                        struct.pack('256s', ifname[:15]))[20:24])
    return addr
def get_a_sql_cur_forever(mylog_i):
    while True:
        try:
            (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
            if None != _cur:
                break
            else:
                mylog_i.info(err)

        except Exception,e:
            mylog_i.info(str(e))
        time.sleep(20)
    return _cur


class led_displayer_udp_server(threading.Thread):
    def __init__(self):
        self.__logger = wtclib.create_logging('../log/leddisplog/udpserver.log')
        threading.Thread.__init__(self)
    def run(self):
        while True:
            self.__logger.info("udp is running start")
            _cur = get_a_sql_cur_forever(self.__logger)

            _udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            ADDR = ('', 5266)
            _udp_sock.bind(ADDR)
            start_time = time.time()
            udp_cnt = 0
            _udp_sock.settimeout(60)
            self.__logger.info(ADDR)
            while True:
                try:
                    (data, addr) = _udp_sock.recvfrom(1024)
                except Exception, e:
                    self.__logger.warning(str(e))
                    #time.sleep(10)
                    continue
                self.__logger.debug(data)
                info = []
                info = analyze_udp_info2dict(data)
                if None != info:
                    info.append(addr[0])
                    info.append(addr[1])
                    if len(info) > 16:
                        if 0 != update_udp_into2sql(self.__logger, info, _cur):
                            self.__logger.error("mysql server has gone away :(")
                            _cur = get_a_sql_cur_forever(self.__logger)

                msg = "nothing"
                _udp_sock.sendto(msg, addr)
                udp_cnt += 1
                if time.time() - start_time > 60:
                    start_time = time.time()
                    self.__logger.info("%d udp broadcast in 60sec"%udp_cnt)
                    udp_cnt = 0

def Get_Screen_special_info(ScreenSN, carport, cur):
    try:
        a1 = cur.execute("select * from ScreenSpecialConfigTable where ScreenSn='%s'"%ScreenSN)
        if 0 == a1:
            return -1,''
        _specials = cur.fetchmany(a1)
    except Exception, e:
        print str(e)
        return -2,''

    _ret = 0
    for _sp in _specials:
        if _sp[1] == ">":
            if carport > _sp[2]:
                _ret = 1
                break
        elif _sp[1] == '<':
            if carport < _sp[2]:
                _ret = 2
                break
        elif _sp[1] == '=':
            if carport == _sp[2]:
                _ret = 3
                break
        elif _sp[1] == '<>':
            if carport != _sp[2]:
                _ret = 4
                break
        elif _sp[1] == "BT":
            if carport > _sp[2] and carport <_sp[3]:
                _ret = 5
                break

    if 0 == _ret or '' == _sp[4] or None == _sp[4]:
        return -3,''
    else:
        return 0, "%s" % _sp[4]



def get_count_carport_msg(ledsql, cur):
    msg = "LEDREGIONSDISPLAY %d 1 1 "%ledsql[12]
    try:
        if 0 == cur.execute("select * from ScreenConfigTable where ScreenSn='%s'"%ledsql[1]):
            return -5, "no %s"%ledsql[1]
        _ScreenConfig = cur.fetchone()
    except Exception, e:
        return -1,  "exp 1"

    msg += "%s %s %s "%(_ScreenConfig[2], _ScreenConfig[3], _ScreenConfig[4])
    localtimeN = time.localtime()
    for i in range(int(_ScreenConfig[4])):
        _a1 = 0
        try:
            _sql_str = "select * from ScreenRegionConfigTable where RegionSn=%d"%_ScreenConfig[5+i]
            _regionConf = cur.execute(_sql_str)
            if 0 == _regionConf:
                return -2,"No RegionSn"
            _ScreenRegionConf = cur.fetchone()
            if "\"%c\"" == _ScreenRegionConf[8]:
                _sql_str = "select count(*) from SpaceStatusTable where CarportStatus=0 and reserved=0 " \
                           "and Spaceid in (select Spaceid from Space2LedTable where RegionSn=%d)" \
                           "" % _ScreenConfig[5 + i]
                _a1 = cur.execute(_sql_str)
                if 0 == _a1:
                    _spaces = 99
                else:
                    _spaces, = cur.fetchone()

            else:
                _spaces = 99
        except Exception,e:
            return -1, 'exp 2'

        msg_dis = "%d %d %d %d %d %d " % (_ScreenRegionConf[1], _ScreenRegionConf[2], _ScreenRegionConf[3],
                                          _ScreenRegionConf[4],_ScreenRegionConf[5], _ScreenRegionConf[6])

        if 2 == _ScreenRegionConf[7]:
            if 0 == _spaces:
                msg_dis += "1 "
            else:
                msg_dis += "0 "
        else:
            msg_dis += "%d " % _ScreenRegionConf[7]

        msg1 = ''
        if "\"%c\"" == _ScreenRegionConf[8]:
            """
            a1 = cur.fetchmany(cur.execute("select count(*) from SpaceStatusTable where CarportStatus=0 and reserved = 0 
            and Spaceid "
                        "in (select Spaceid from Space2LedTable where RegionSn in "
                        "(select RegionSn from ScreenRegionConfigTable as Led where RegionSn=%d))" % (
                        _ScreenConfig[5 + i])))[0]"""
            _ret = -1
            if 0 != _ScreenConfig[30]:
                _ret, msg1 = Get_Screen_special_info(_ScreenConfig[0], _spaces, cur)
            if 0 != _ret:
                if 3 == _ScreenConfig[29]:
                    msg1 = "%03d"%(_spaces)
                elif 4 == _ScreenConfig[29]:
                    msg1 = "%04d" % (_spaces)
                elif 2 == _ScreenConfig[29]:
                    msg1 = "%02d" % (_spaces)
                else:
                    msg1 = "%d" % (_spaces)
        else:
            if _ScreenRegionConf[8].find('%') >= 0:
                str1 = _ScreenRegionConf[8].strip('\"')
                per = 0
                while True:
                    per += str1[per:].find('%')
                    if per < 0:
                        break
                    per2 = str1[per+2:].find('%')
                    if "h" == str1[per+1:per+2]:
                        msg1 += "%d" % (localtimeN.tm_hour)
                    elif "m" == str1[per+1:per+2]:
                        msg1 += "%02d" % (localtimeN.tm_min)
                    elif "w" == str1[per+1:per+2]:
                        msg1 += "%02d" % (localtimeN.tm_wday + 1)

                    elif "Y" == str1[per+1:per+2]:
                        msg1 += "%d" % (localtimeN.tm_year)
                    elif "M" == str1[per+1:per+2]:
                        msg1 += "%d" % (localtimeN.tm_mon)
                    elif "D" == str1[per+1:per+2]:
                        msg1 += "%d" % (localtimeN.tm_mday)

                    if per2 < 0:
                        msg1 += str1[per+2:]
                    else:
                        msg1 += str1[per+2 : per+2+per2]

                    per += 2
                    if per >= len(str1):
                        break

            else:
                msg1 = _ScreenRegionConf[8].strip("\"")
        msg_dis += msg1 + '\t'
        try:
            cur.execute("update ScreenConnectTable set display%d='%s' where ScreenSn='%s'"%(i+1,msg_dis,_ScreenConfig[0]))
        except Exception, e:
            return -1, 'exp 3'
        msg += msg_dis
    _xor_val = 0
    for datai in msg:
        _xor_val = _xor_val ^ ord(datai)
    msg += "%02X\r\n"%_xor_val
    return 0, msg


class led_displayer_tcp_client(threading.Thread):
    def __init__(self, num):
        self.__id = num
        self.__logger = wtclib.create_logging('../log/leddisplog/tcpclient%d.log' % num)

        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret
        self.__logger.info("running start")
        _cur = get_a_sql_cur_forever(self.__logger)
        self.__logger.info("tcp%d get cur"%(self.__id))
        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            self.__logger.info("get queue")
            _recv_dict = json.loads(_recv_json)
            try:
                a1 = _cur.execute("select * from LedDisplayerUdpInfo where LEDID='" + _recv_dict['LEDID'] + "'")
            except Exception,e:
                self.__logger.error(str(e))
                if 'MySQL server has gone away' in str(e):
                    _cur = get_a_sql_cur_forever(self.__logger)
                continue
            if 0 == a1:
                _dic1 = {"ret":0,"err":"no sql info", "id":self.__id}
                self.__logger.warning(json.dumps(_dic1))
                self.__logger.warning(_recv_json)
            elif a1 > 1:
                _dic1 = {"ret": 0, "err": "too many LEDID", "id":self.__id}
                self.__logger.warning(json.dumps(_dic1))
                self.__logger.warning(_recv_json)
            else:
                try:
                    ledsql = _cur.fetchone()
                except Exception,e:
                    self.__logger.error(str(e))
                    if 'MySQL server has gone away' in str(e):
                        _cur = get_a_sql_cur_forever(self.__logger)
                    continue

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    address = (ledsql[16], 5813)
                    sock.connect(address)
                    (_ret, msg) = get_count_carport_msg(ledsql, _cur)
                    #if _ret < 0:
                    #    _cur = get_a_sql_cur_forever()
                    if 0 == _ret:
                        sock.sendall(msg)
                        sock.setblocking(0)
                        for i in range(5):
                            time.sleep(0.02)
                            _data_recv = sock.recv(1024)
                            if 0 != len(_data_recv):
                                break
                        self.__logger.info(msg+" @%s %s"%(ledsql[1], _data_recv))
                        _dic1 = {"ret": 1, "id":self.__id}
                        if 0 != len(_data_recv):
                            _recv = _data_recv.split(' ')
                            if "LEDREGIONSDISPLAY" == _recv[0]:
                                if len(_recv) > 2:
                                    _sql_str = "update ScreenConnectTable set returnval='%s %s'"\
                                               %(_recv[1],_recv[2])
                                else:
                                    _sql_str = "update ScreenConnectTable set returnval='%s'"%(_recv[1])
                                _sql_str += " where ScreenSn='%s'"%ledsql[1]
                                _cur.execute(_sql_str)
                    else:
                        _dic1 = {"ret": 0, "id": self.__id, "err":msg}
                        cur.execute("update ScreenConnectTable set returnval='%s' where ScreenSn='%s'"%(msg, ledsql[1]))
                        self.__logger.info("get msg error = "+msg)
                except Exception, e:
                    _dic1 = {"ret":0, "err":str(e), "id":self.__id}
                    self.__logger.error("LEDID:%s,ip=%s"%(ledsql[1], ledsql[16]))
                    self.__logger.error(str(e))
                try:
                    sock.close()
                except Exception, e:
                    self.__logger.info("socket close "+str(e))
            _recv_dict.update(_dic1)
            gQueue_ret.put(json.dumps(_recv_dict))
            self.__logger.info("tcp client%d:%s"%(self.__id, json.dumps(_recv_dict)))


def make_some_virtualLeds_indb(cur):
    for i in range(123456, 123468):
        cur.execute("insert into LedDisplayerUdpInfo(LEDID, IPaddress) values('%d', '192.168.7.18')"%i)
    #for i in range(123556, 123560):
    #    cur.execute("insert into LedDisplayerUdpInfo(LEDID, IPaddress) values('%d', '192.168.8.18')"%i)




def create_qld_db(cur):
    try:
        cur.execute("create table if not exists LedDisplayerUdpInfo("
                    "id int not null auto_increment primary key,"  # 0  
                    "LEDID char(16) , "         #1
                    "width smallint,"               #2
                    "height smallint,"              #3
                    "unitSum tinyint,"              #4
                    "distanceP2P char(8),"          #5
                    "color char(16),"               #6
                    "definition char(16),"          #7
                    "minPix char(8),"               #8
                    "productName char(16),"         #9
                    "HardwareVersion char(16),"     #10
                    "softwareVersion char(16),"     #11
                    "currentSerialNo int,"     #12
                    "MAC char(24),"                 #13
                    "refresh char(4),"              #14
                    "systemFlag char(8),"           #15
                    "IPaddress char(24),"           #16
                    "port int,"                     #17
                    "ErrorFlag tinyint default 0,"  #18
                    "time DATETIME"  # 1            
                    ")engine=memory")  # 17
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        pass
    #make_some_virtualLeds_indb(cur)
    try:
        cur.execute("create table if not exists LedDisplayerUdpErrorInfo("
                    "id int not null auto_increment primary key,"
                    "LEDID char(16),"  # 0
                    "width smallint,"
                    "height smallint,"
                    "unitSum tinyint,"
                    "distanceP2P char(8),"
                    "color char(16),"
                    "definition char(16),"
                    "minPix char(8),"
                    "productName char(16),"
                    "HardwareVersion char(16),"
                    "softwareVersion char(16),"
                    "currentSerialNo int,"
                    "MAC char(24),"
                    "refresh char(4),"
                    "systemFlag char(8),"
                    "IPaddress char(24), "
                    "port int,"
                    "ErrorFlag tinyint default 0,"
                    "time DATETIME"  # 1
                    ")engine=memory")  # 17
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        pass

def get_root_dir_config():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        #mylog.error(str(e))
        return None
    secs = cf.sections()
    try:
        opts = cf.options("file_save")
    except Exception, e:
        #mylog.error(str(e) + ' file_save')
        return None
    try:
        dirs = cf.get("file_save", "root_dir")
        return dirs
    except Exception, e:
        #mylog.error(str(e) + ' get file_save')
        return None


if __name__ == '__main__':
    if not os.path.isdir("../log/leddisplog"):
        try:
            os.mkdir("../log/leddisplog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    time.sleep(10)
    mylog = wtclib.create_logging("../log/leddisplog/ledplayer.log")
    mylog.info("start")

    cur = get_a_sql_cur_forever(mylog)
    create_qld_db(cur)
    #mylog.warning(cur.connection)
    #mylog.warning(cur.messages)
    if None == cur:
        mylog.error("connect to db fail")
        os._exit()
    thread = led_displayer_udp_server()
    thread.start()
    """"""
    #time.sleep(25)
    thread_idles = THREAD_NUM

    gThread_using_flag = []
    threads = []
    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = led_displayer_tcp_client(i)
        thread.start()
        time.sleep(0.1)
        threads.append(thread)
    while True:
        leds = cur.execute("select * from LedDisplayerUdpInfo")
        if 0 == leds:
            time.sleep(5)
            continue
        else:
            break
    _pid = os.getpid()
    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 300, %d,'%s')" % (_pid, __file__, int(time.time()),ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "ledplayer" in _dic1:
            _version = _dic1["ledplayer"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ledplayer','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylog.error(str(e) )
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylog)

    while True:

        _timeSec = time.time()
        mylog.debug("start time=%f"%_timeSec)
        try:
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(_timeSec), _pid,ServerID))
        except Exception, e:
            mylog.error(str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylog)

        #_timeSec = time.time()
        try:
            leds = cur.execute("select * from LedDisplayerUdpInfo")
            ledsinfo = cur.fetchall()
        except Exception, e:
            ledsinfo = None
            mylog.error(str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylog)
            continue
        if None != ledsinfo:
            for led in ledsinfo:
                if 0 != led[18]:  #ErrorFlag
                    mylog.warning(led[1]+" ErrorFlag=%d"%led[18])
                    continue
                try:
                    if 0 == cur.execute("select * from ScreenConnectTable where ScreenSn='%s'"%led[1]):#not for connect ctrl
                        continue
                except Exception, e:
                    mylog.error(str(e))
                    break
                mylog.info("refresh %s"%(led[1]))

                try:
                    refresh_time = time.mktime(led[19].timetuple())
                    if _timeSec - refresh_time > 60:
                        mylog.warning("led udp time is %s and now is %s" % (led[19], datetime.datetime.now()))
                        continue
                except:
                    mylog.warning("led udp time is %s and now is %s"%(led[19],datetime.datetime.now()))

                _dic = {"LEDID":led[1]}
                _ret = 0
                for i in range(THREAD_NUM):
                    if 0 != gThread_using_flag[i]:
                        gQueues[i].put_nowait(json.dumps(_dic))
                        gThread_using_flag[i] = 0
                        _ret = 1
                        break
                if 0 != _ret:
                    continue
                else:
                    rec_json = gQueue_ret.get(block=True)
                    gQueues[json.loads(rec_json)["id"]].put_nowait(json.dumps(_dic))
                    #gThread_using_flag[json.loads(rec_json)["id"]] = 1
        mylog.debug("end queue time=%f"%time.time())
        timeused = time.time() - _timeSec
        mylog.info("process leddisplayer %d leds in %f second"%(leds, timeused))
        if timeused < 3:
            time.sleep(3-timeused)
        Cur_qsize = gQueue_ret.qsize()
        #_queue_start_time = time.time()
        for i in range(Cur_qsize):
            rec_json = gQueue_ret.get(block=True)
            gThread_using_flag[json.loads(rec_json)["id"]] = 1
        #mylog.debug("between queue get %f second"%(time.time()-_queue_start_time))