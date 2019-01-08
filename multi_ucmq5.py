import ConfigParser
import Queue
import json
import math
import os
import socket
import sys
import threading
import time
import urllib
import urllib2

import MySQLdb
import pika

from bin import wtclib

"""receive ucmq messages and download the files to local
"""
DIRECTION_SAVE_FILES = "../../waiting/"
THREAD_NUM = 5 #how many threads
global mylogger
gQueues = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)



Rabbitmq_Place_exchange = "123"
Rabbitmq_Plate_exchange = "1235"
Rabbitmq_Place_router_key = "sdf"
Rabbitmq_Plate_router_key = "iuh"

"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET
"""

def check_parser_ucmq_cmd(jstr):
    return 0, "abc"

def ucmq_put_msg(dic, ucmq_url):

    _test_data2 = {'name': 'userjpg', 'opt': 'put', 'ver': '2', 'data': json.dumps(dic)}
    _test_data_encode2 = urllib.urlencode(_test_data2)
    _ucmqIP = ucmq_url[ : ucmq_url.find('?')]
    res_data = urllib2.urlopen(_ucmqIP + "?" + _test_data_encode2)
    res = res_data.read()
    res_data.close()
    urllib.urlcleanup()

pic_sn = 0

def check_download_filename(jstr, ucmq_url):
    global pic_sn
    _dic1 = json.loads(jstr)
    if not "ip" in _dic1:
        return 0, "ip"
    if not "location" in _dic1:
        return 0, "location"
    if not "type_for" in _dic1:
        return 0, "type_for"
    if not "pic_sn" in _dic1:
        return 0, "pic_sn"
    if not "why" in _dic1:
        return 0, "why"
    if not "sn" in _dic1:
        return 0, "sn"
    if not "CMOS" in _dic1:
        return 0, "CMOS"


    _path = DIRECTION_SAVE_FILES + _dic1["sn"] +'/'
    if not os.path.isdir(_path):
        try:
            os.mkdir(_path)
        except Exception, e:
            if not os.path.isdir(_path):
                mylogger.error(_path+str(e))
                return 0, str(e)
    s = os.getcwd()
    _top_top = s[:s[0:s.rfind('/')].rfind('/')]
    fl = time.time()
    (fraction1, inter1) = math.modf(fl)
    sec = "%d_%d" % (int(inter1), pic_sn)
    pic_sn +=1
    del fl, fraction1, inter1
    _path = _top_top + '/waiting/' + _dic1["sn"] +'/' + sec + _dic1["location"][_dic1["location"].rfind('.'):]
    if "place" == _dic1["type_for"]:
        ucmq_put_msg(_dic1, ucmq_url)   #renew a user.jpg
    del _dic1
    return 1, _path




def ucmq_get_msg(ucmq_url):
    global mylogger

    while True:
        try:
            res_data = urllib2.urlopen(ucmq_url)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylogger.info(str(e))
            time.sleep(20)
            continue
        break
    try:
        res = res_data.read()
        mq_str = res.split('\n')
        #print mq_str[0]
        ret_str = mq_str[0].rstrip('\r')
        if (ret_str != "UCMQ_HTTP_OK"):
            mq_str[1] = None
        res_data.close()
        urllib.urlcleanup()
        return mq_str[1]
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        return None

class DownloadThread(threading.Thread):
    def __init__(self, idnum):
        self.__id = idnum
        self.__url_addr = []
        self.__file_name = []
        self.__pic_type = []
        self.__logger = wtclib.create_logging('../log/downfilelog/thread%d.log' % idnum)
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret

        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            _recv_dict = json.loads(_recv_json)
            self.__url_addr = "http://" + _recv_dict["ip"] + _recv_dict["location"]
            """
            fl = time.time()
            (fraction1, inter1) = math.modf(fl)
            sec = "%d_%d"%(int(inter1), int(1000*fraction1))
            del fl, fraction1, inter1"""
            self.__file_name = _recv_dict["path"]# + sec +".jpg"
            #print "Child id=" + str(self.__id)+ str(time.time()) +"get url=" + str(self.__url_addr) +" save to " + str(self.__file_name)
            step = 1
            try:
                fd, info = urllib.urlretrieve(url=self.__url_addr, filename= self.__file_name)
            except Exception, e:
                step = -1
                ret_str = str(e)
                self.__logger.warning(str(e)+self.__url_addr)
            finally:
                if step > 0:
                    if "content-length" in info.dict:
                        _ret_dic = {"ret": 1, "id": self.__id}
                    else:
                        os.remove(self.__file_name)
                        self.__logger.warning("no content-length, download " + self.__file_name +" failed")
                        _ret_dic = {"ret": "no content-length", "id": self.__id}

            #        gQueue_ret.put(json.dumps({"ret": 1, "id": self.__id, "filename":self.__file_name, "pic_type":_recv_dict["pic_type"]}))
                else:
                    _ret_dic = {"ret":ret_str, "id": self.__id}
            #        gQueue_ret.put(json.dumps({"ret": ret_str, "id": self.__id}))
                _recv_dict.update(_ret_dic)
                gQueue_ret.put(json.dumps(_recv_dict))
                #print "child end  id=" + str(self.__id) +" time="+ str(time.time())
                self.__logger.debug("child end  id=" + str(self.__id) +" time="+ str(time.time()))

def get_place_rabbitmq_channel():
    global mylogger
    while True:
        try:
            credentials = pika.PlainCredentials("guest", "guest")
            conn_params = pika.ConnectionParameters(host="localhost", virtual_host="/", credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="place", exchange_type="direct",
                             passive=False, durable=True, auto_delete=False)
    return channel

def get_plate_rabbitmq_channel():
    global mylogger
    while True:
        try:
            credentials = pika.PlainCredentials("guest", "guest")
            conn_params = pika.ConnectionParameters(host="localhost", virtual_host="/", credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="plate", exchange_type="direct",
                             passive=False, durable=True, auto_delete=False)
    return channel

def get_a_rabbitmq_channel():
    global Rabbitmq_Place_exchange, Rabbitmq_Plate_exchange
    global Rabbitmq_Place_router_key, Rabbitmq_Plate_router_key

    _cf = ConfigParser.ConfigParser()
    try:
        _cf.read("../conf/conf.conf")
    except Exception, e:
        mylogger.error(str(e))
        return 0
    _secs = _cf.sections()
    try:
        _opts = _cf.options("rabbitmq")
    except Exception, e:
        mylogger.error(str(e)+' rabbitmq')
        return 0
    try:
        _Place_host = _cf.get("rabbitmq", "placemq_server_addr")
        _Place_port = _cf.getint("rabbitmq", "placemq_server_port")
        Rabbitmq_Place_exchange = _cf.get("rabbitmq", "placemq_exchange")
        _Place_exchange_type = _cf.get("rabbitmq", "placemq_exchange_type")
        Rabbitmq_Place_router_key = _cf.get("rabbitmq", "placemq_router_key")
        _Place_user_name = _cf.get("rabbitmq", "placemq_user_name")
        _Place_passwd = _cf.get("rabbitmq", "placemq_passwd")
    except Exception, e:
        mylogger.error(str(e)+' get placemq')
        return 0

    try:
        _Plate_host = _cf.get("rabbitmq", "platemq_server_addr")
        _Plate_port = _cf.getint("rabbitmq", "platemq_server_port")
        Rabbitmq_Plate_exchange = _cf.get("rabbitmq", "platemq_exchange")
        _Plate_exchange_type = _cf.get("rabbitmq", "platemq_exchange_type")
        Rabbitmq_Plate_router_key = _cf.get("rabbitmq", "platemq_router_key")
        _Plate_user_name = _cf.get("rabbitmq", "platemq_user_name")
        _Plate_passwd = _cf.get("rabbitmq", "platemq_passwd")
    except Exception, e:
        mylogger.error(str(e)+' get placemq')
        return 0
    del _cf
    #credentials = pika.PlainCredentials(RabbitMQ_user, RabbitMQ_passwd)
    if _Place_host == _Plate_host and _Place_user_name == _Plate_user_name \
            and _Place_passwd == _Plate_passwd and _Place_port == _Plate_port:
        try:
            credentials = pika.PlainCredentials(_Place_user_name, _Place_passwd)
        #conn_params = pika.ConnectionParameters(host="192.168.7.19", port=5672, credentials=credentials)
            conn_params = pika.ConnectionParameters(host= _Plate_host,port=_Place_port, credentials=credentials)
            conn_broker = pika.BlockingConnection(conn_params)
            _Place_channel = conn_broker.channel()
            _Place_channel.exchange_declare(exchange=Rabbitmq_Place_exchange, exchange_type=_Place_exchange_type,
                                 passive=False, durable=True, auto_delete=False)
            _Plate_channel = conn_broker.channel()
            _Plate_channel.exchange_declare(exchange=Rabbitmq_Plate_exchange, exchange_type=_Plate_exchange_type,
                                            passive=False, durable=True, auto_delete=False)
        except Exception, e:
            mylogger.error(str(e)+"rabbitmq")
            return None, None
    else:
        return None, None
    return _Place_channel, _Plate_channel


def get_a_sql_cur():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("../conf/conf.conf")
    except Exception, e:
        mylogger.error(str(e))
        return None
    secs = cf.sections()
    try:
        opts = cf.options("db")
    except Exception, e:
        mylogger.error(str(e)+' db')
        return None
    try:
        DB_host = cf.get("db", "location")
        DB_user = cf.get("db", "user_name")
        DB_passwd = cf.get("db", "user_passwd")
        DB_name = cf.get("db", "name")
    except Exception, e:
        mylogger.error(str(e)+' get db')
        return None
    while True:
        try:
            conn = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_passwd, db=DB_name)
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except:
            time.sleep(20)
            mylogger.warn("Can't connect to MySQL")

    return cur



def maybe_add_a_new_device(json_str, cur):
    _dic1 = json.loads(json_str)
    if not "ip" in _dic1:
        print "not ip in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return None


    if not "slave" in _dic1:
        print "not slace in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return
    elif not type(_dic1["slave"])==int:
        print "not type slave is int" + " in line:" + str(sys._getframe().f_lineno)
        return None

    if not "sn" in _dic1:
        print "not sn in _dic1"
        return None


    if not "exp" in _dic1:
        print "not exp in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return None

    if not "gain" in _dic1:
        print "not gain in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return None


    _cmos = 0
    if "CMOS" in _dic1 and type(_dic1["CMOS"])==int:
        _cmos = _dic1["CMOS"]

    _neighbor = ''
    if "neighbor" in _dic1:
        _neighbor = _dic1["neighbor"]
    _BTsn = ''
    if "bluetooth" in _dic1:
        _BTsn = _dic1["bluetooth"]
    _MAC_addr = ''
    if "MAC" in _dic1:
        _MAC_addr = _dic1["MAC"]

    try:
        if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%((_dic1["sn"], _cmos))):
            for i in range(_cmos+1):
                cur.execute("insert into hvpdEquipmentsTable(cameraID, cmosID, Mac, newCameraFlag)"
                        "values ('%s', %d, '%s', 2)ON DUPLICATE KEY UPDATE Mac='%s'"%(_dic1["sn"], i, _MAC_addr, _MAC_addr))
                cur.execute("insert into OnlineHvpdStatusTableMem(cameraID, cmosID, neighbor_camera, slave, ip, exp, gain, CMOS, bluetooth, "
                            "LatestConnect) values ('%s', %d, '%s', %d, '%s', %s, %s, %d, '%s', now())"
                            % (_dic1["sn"], i, _neighbor, _dic1["slave"], _dic1["ip"],
                               _dic1["exp"], _dic1["gain"], i, _BTsn))
        else:
            cur.execute("update OnlineHvpdStatusTableMem set neighbor_camera='%s', slave=%d, ip='%s',exp=%s,gain=%s,CMOS=%d, "
                        "bluetooth='%s',LatestConnect=now() where cameraID='%s' and cmosID=%d"
                        % (_neighbor, _dic1["slave"], _dic1["ip"],_dic1["exp"], _dic1["gain"], _cmos, _BTsn, _dic1["sn"], _cmos))

        if '' == _neighbor:
            if 0 == cur.execute("select * from Equipment2cameraIdMem where equipmentID='%s'"%_dic1["sn"]):
                if 0 == _cmos:
                    cur.execute("insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, ReNewFlag)values('%s', '%s',0, 2)"
                                %(_dic1["sn"], _dic1["sn"]))
                else:
                    cur.execute("insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2, "
                                "ReNewFlag)values('%s', '%s',0, '%s',1, 2)"% (_dic1["sn"], _dic1["sn"], _dic1["sn"]))
            """
            else:
                if 0 == _cmos:
                    cur.execute("update Equipment2cameraIdMem set cameraID1='%s' where equipmentID='%s'"%(_dic1["sn"], _dic1["sn"]))
                else:
                    cur.execute("update Equipment2cameraIdMem set cameraID2='%s' where equipmentID='%s'"%(_dic1["sn"], _dic1["sn"]))
            """
            if 0 == cur.execute("select * from LampSettingTableMem where equipmentID='%s'"%_dic1["sn"]):
                if 0 == _cmos:
                    cur.execute("insert into LampSettingTableMem(equipmentID, ReNewFlag, CtrlTableName, SpaceAll, Space1ID, "
                                "Space2ID, Space3ID, ManualCtrFlag)"
                                "values('%s', 2, 'defaultXspace', 3, '%s', '%s', '%s', 0)"
                                %(_dic1["sn"], _dic1["sn"]+'1', _dic1["sn"]+'2', _dic1["sn"]+'3'))
                else:
                    cur.execute(
                        "insert into LampSettingTableMem(equipmentID, ReNewFlag, CtrlTableName, SpaceAll, Space1ID, "
                        "Space2ID, Space3ID, Space4ID, Space5ID, Space6ID, ManualCtrFlag)"
                        "values('%s', 2, 'defaultXspace', 6, '%s', '%s', '%s', '%s', '%s', '%s', 0)"
                        % (_dic1["sn"], _dic1["sn"] + '1', _dic1["sn"] + '2', _dic1["sn"] + '3',
                           _dic1["sn"] + '4', _dic1["sn"] + '5', _dic1["sn"] + '6'))
            if 0 == cur.execute("select * from hvpd2LampSettingTableMem where cameraID='%s' and cmosID=%d"%(_dic1["sn"], _cmos)):
                cur.execute("insert into hvpd2LampSettingTableMem(cameraID,cmosID, ReNewFlag, Effect1EquipID)"
                            "values('%s', %d, 2, '%s')"%(_dic1["sn"], _cmos, _dic1["sn"]))
            if 0 != _cmos:
                if 0 == cur.execute("select * from SpaceStatusTable where Spaceid='%s'"%(_dic1["sn"]+'4')):
                    for i in range(4, 7):
                        try:
                            cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, cmosID, CarportStatus)"
                                        "values('%s', '%s',1,0)"%((_dic1["sn"]+str(i)), _dic1["sn"]))
                        except Exception, e:
                            print str(e) + " in line: " + str(sys._getframe().f_lineno)
                            continue

        else:
            if 0 == cur.execute("select * from Equipment2cameraIdMem where equipmentID='%s'"%(min(_dic1["sn"], _neighbor))):
                cur.execute("insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2, cmosID2, "
                            "ReNewFlag)values('%s', '%s', 0, '%s', 0, 2)"
                            %(min(_dic1["sn"], _neighbor), _dic1["sn"], _neighbor))
            if 0 == cur.execute("select * from LampSettingTableMem where equipmentID='%s'"%min(_dic1["sn"], _neighbor)):
                cur.execute("insert into LampSettingTableMem(equipmentID, ReNewFlag, CtrlTableName, SpaceAll, Space1ID, "
                            "Space2ID, Space3ID, Space4ID, Space5ID, Space6ID, ManualCtrFlag)"
                            "values('%s', 2, 'defaultXspace', 6, '%s', '%s', '%s', '%s', '%s', '%s', 0)"
                            %(min(_dic1["sn"], _neighbor), _dic1["sn"]+'1', _dic1["sn"]+'2', _dic1["sn"]+'3', _neighbor+'1',
                              _neighbor+'2', _neighbor+'3'))
            if 0 == cur.execute("select * from hvpd2LampSettingTableMem where cameraID='%s' and cmosID=%d"%(_dic1["sn"],_cmos)):
                cur.execute("insert into hvpd2LampSettingTableMem(cameraID, cmosID, ReNewFlag, Effect1EquipID)"
                            "values('%s', %d, 2, '%s')"%(_dic1["sn"], _cmos, min(_dic1["sn"], _neighbor)))

            if 0 == cur.execute("select * from SpaceStatusTable where Spaceid='%s'"%(_neighbor+'1')):
                for i in range(1, 4):
                    try:
                        cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, cmosID, CarportStatus)"
                                    "values('%s', '%s',0,0)" % ((_neighbor + str(i)), _neighbor))
                    except Exception, e:
                        print str(e) + " in line: " + str(sys._getframe().f_lineno)
                        continue

        if 0 == cur.execute("select * from SpaceStatusTable where Spaceid='%s'"%(_dic1["sn"]+'1')):
            for i in range(1,4):
                try:
                    cur.execute("insert into SpaceStatusTable(Spaceid, cameraID, cmosID, CarportStatus)"
                                "values('%s', '%s',0,0)" % ((_dic1["sn"] + str(i)), _dic1["sn"]))
                except Exception, e:
                    print str(e) + " in line: " + str(sys._getframe().f_lineno)
                    continue
        a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%(_dic1["sn"], _cmos))
        return cur.fetchmany(a1)[0]
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        return None

def HDCD_ucmq_cmd_process(jstr):
    return

def make_rabbitmq_msg(json_str, filename, sql):
    _dic = json.loads(json_str)

    info = {"cam_id":_dic["sn"],"pic_full_name":filename,
            "Pic_type_for":_dic["why"], "CMOS":_dic["CMOS"]}

    return info

def make_PlateRabbitmq_msg(json_str, sql):
    _dic = json.loads(json_str)

    info = {"cam_id":_dic["sn"],"pic_full_name":_dic["path"],
            "Pic_type_for":_dic["why"], "CMOS":_dic["CMOS"],
            "LTx":_dic["LTx"], "LTy":_dic["LTy"],
            "RBx":_dic["RBx"], "RBy":_dic["RBy"],
            "plateGet":_dic["plateGet"]}

    return info

def Load_camera_table2Mem(cur):
    try:
        cur.execute("TRUNCATE TABLE OnlineHvpdStatusTableMem")
    #cur.execute("TRUNCATE TABLE Equipment2cameraIdMem")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
    """
    _a1 = cur.execute("select * from hvpdEquipmentsTable")
    if 0 != _a1:
        _tables = cur.fetchmany(_a1)
        for table in _tables:
            cur.execute("insert into ()values()ON DUPLICATE KEY UPDATE ")
    """

if __name__ == '__main__':
    global mylogger
    if not os.path.isdir("../log/downfilelog"):
        try:
            os.mkdir("../log/downfilelog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    #mylogger = create_logging("downfilelog/Mthread.log")
    mylogger = wtclib.create_logging("../log/downfilelog/Mthread.log")
    mylogger.info("start running")
    if not os.path.isdir(DIRECTION_SAVE_FILES):
        try:
            os.mkdir(DIRECTION_SAVE_FILES)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylogger.error(str(e))
            os._exit()

    (val, _ucmq_url) = wtclib.get_ucmq_url(None)
    if 0 == val:
        mylogger.error("can not get ucmq url return "+ _ucmq_url)
        os._exit()
    del val
    #(Aimq, Remq) = get_a_rabbitmq_channel()
    Aimq = get_place_rabbitmq_channel()
    Remq = get_plate_rabbitmq_channel()
    if None == Aimq:
        mylogger.error("can get rabbitmq")
        os._exit()

    mylogger.info(Aimq)
    print Aimq
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    """
    js_msg = "shfioyh23u792678568456"
    js_msg2 = "6496494949849849"
    for i in range(10):
        Aimq.basic_publish(body=js_msg, exchange=Rabbitmq_Place_exchange, properties=msg_props,
                       routing_key=Rabbitmq_Place_router_key)
        Remq.basic_publish(body=js_msg2, exchange=Rabbitmq_Plate_exchange, properties=msg_props,
                           routing_key=Rabbitmq_Plate_router_key)"""

    socket.setdefaulttimeout(10)
    j = 2000

    cur = get_a_sql_cur()
    if None == cur:
        mylogger.error("config fail with db")
    Load_camera_table2Mem(cur)
    print time.time()
    threads = []
    thread_idles = THREAD_NUM

    gThread_using_flag = []
    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = DownloadThread(i)
        thread.start()
        threads.append(thread)
    _queue_block = False
    sleep_sec = 0.5
    #ret_val = 0
    sec_start = time.time()
    _mysql_link_timet = sec_start
    _place_rabbitmq_timet = sec_start
    _plate_rabbitmq_timet = sec_start
    _pid = os.getpid()
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 180, %d)"%(_pid, __file__, (time.time())))
    except Exception, e:
        mylogger.error(str(e)+time.asctime())

    while True:
        _timeSec = int(time.time())
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d"%(_timeSec, _pid))#wdi

        json_str = None
        _ucmq_loop = 12
        if thread_idles >= THREAD_NUM:
            thread_idles = THREAD_NUM#all thread is idle
            while True:
                json_str = ucmq_get_msg(_ucmq_url)
                if None != json_str:
                    break
                else:
                    time.sleep(0.5)
                _ucmq_loop -= 1
                if 0 == _ucmq_loop:
                    break
            sleep_sec = 0.02
            _queue_block = False
        elif 0 == thread_idles:   #all thread is busy
            _queue_block = True     #queue get block,until a thread is idle
        else:       #some thread is idle
            _queue_block = False
            json_str = ucmq_get_msg(_ucmq_url)

        mylogger.debug("thread_idle = %d"%thread_idles)
        if isinstance(json_str, str):
            try:
                json.loads(json_str, encoding='utf-8')
            except:
                json_str = None
        if None != json_str:
            _mysql_link_timet = time.time()
            sql_info = maybe_add_a_new_device(json_str, cur)
            if None == sql_info:
                continue
            ret_val = check_download_filename(json_str, _ucmq_url)
            if 1 == ret_val[0]:
                _dic = json.loads(json_str)
                _dic1 = {"path":ret_val[1]}
                _dic.update(_dic1)

                for i in range(THREAD_NUM):
                    if gThread_using_flag[i] == 1:
                        gQueues[i].put_nowait(json.dumps(_dic))
                        gThread_using_flag[i] = 0
                        #print "Queue put to id%d"%i
                        mylogger.debug("Queue put to id%d"%i)
                        break
                thread_idles -= 1
                del _dic1, _dic
            ret_val = check_parser_ucmq_cmd(json_str)
            if 1 == ret_val[0]:
                HDCD_ucmq_cmd_process(json_str)
            del json_str


        rec_json_buff = []
        if True == _queue_block:
            try:
                #print "Queue get blocked"
                rec_json = gQueue_ret.get(block=True)
                gThread_using_flag[json.loads(rec_json)["id"]] = 1
                rec_json_buff.append(rec_json)
                thread_idles += 1
                #print "Queue get blocked"
                mylogger.debug("Queue get blocked "+ rec_json)
            except IOError, Queue.Empty:
                pass
        else:
            Cur_qsize = gQueue_ret.qsize()
            #print "Queue get %d mq"%Cur_qsize
            #mylogger.debug("Queue get %d mq"%Cur_qsize)
            for i in range(Cur_qsize):
                try:
                    rec_json = gQueue_ret.get(block=False)
                    gThread_using_flag[json.loads(rec_json)["id"]] = 1
                    thread_idles += 1
                    rec_json_buff.append(rec_json)

                    #print "Queue get " + rec_json
                    mylogger.debug("Queue get " + rec_json)
                except IOError, Queue.Empty:
                    pass

        for rec_json in rec_json_buff:#
            dic1 = json.loads(rec_json)
            if not "ret" in dic1:
                continue
            if 1 != dic1["ret"]:
                mylogger.debug("ret = 0")
                continue

            if not "type_for" in dic1:
                mylogger.debug("no type_for in dic")
                continue
            if "place" == dic1["type_for"]:
                msg = make_rabbitmq_msg(rec_json, dic1["path"], sql_info)
                js_msg = json.dumps(msg)
                _place_rabbitmq_timet = _timeSec
                try:
                    mylogger.debug("rabbitmq publish: "+js_msg)
                    _place_rabbitmq_timet = _timeSec
                    Aimq.basic_publish(body=js_msg, exchange="place", properties=msg_props,
                                          routing_key="place queue")
                except Exception, e:
                    mylogger.debug(str(e))
                    mylogger.debug(Aimq)
                    Aimq = get_place_rabbitmq_channel()
                    #os._exit()
            elif "plate" == dic1["type_for"]:
                if not "plateGet" in dic1:
                    continue
                if not "LTx" in dic1:
                    continue
                if not "LTy" in dic1:
                    continue
                if not "RBx" in dic1:
                    continue
                if not "RBy" in dic1:
                    continue
                msg = make_PlateRabbitmq_msg(rec_json,  sql_info)
                js_msg = json.dumps(msg)
                if dic1["LTx"] < 0 or dic1["LTy"] < 0 or dic1["RBx"] < 0 or dic1["RBy"] < 0:
                    mylogger.error(js_msg)
                    mylogger.error(rec_json)
                mylogger.debug("rabbitmq publish: " + js_msg)
                _plate_rabbitmq_timet = _timeSec
                try:
                    Remq.basic_publish(body=js_msg, exchange="plate", properties=msg_props,
                                          routing_key="plate queue")
                except Exception, e:
                    mylogger.debug(str(e))
                    Remq = get_plate_rabbitmq_channel()
            del dic1

        if _timeSec - _place_rabbitmq_timet > 10:#to keep rabbitmq alive
            try:
                _place_rabbitmq_timet = _timeSec
                js_msg = json.dumps({"msg":"alive"})
                mylogger.debug("rabbitmq publish:place "+js_msg)
                Aimq.basic_publish(body=js_msg, exchange="place", properties=msg_props,
                                   routing_key="place queue")
            except Exception, e:
                mylogger.debug(str(e))
                mylogger.debug(Aimq)
                Aimq = get_place_rabbitmq_channel()

        if _timeSec - _plate_rabbitmq_timet > 10:
            try:
                _plate_rabbitmq_timet = _timeSec
                js_msg = json.dumps({"msg":"alive"})
                mylogger.debug("rabbitmq publish:plate "+js_msg)
                Remq.basic_publish(body=js_msg, exchange="plate", properties=msg_props,
                                   routing_key="plate queue")
            except Exception, e:
                mylogger.debug(str(e))
                mylogger.debug(Aimq)
                Remq = get_plate_rabbitmq_channel()

        #del  js_msg
        time.sleep(sleep_sec)
        #print "sleep ",sleep_sec
        #mylogger.debug("sleep %f"%sleep_sec)

        #j -= 1
    print "exit ",time.time(), "start @", sec_start
    exit()