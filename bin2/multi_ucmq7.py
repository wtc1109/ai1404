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
import datetime
import MySQLdb
import pika
import wtclib
import random,shutil

"""receive ucmq messages and download the files to local
"""
DIRECTION_SAVE_FILES = "/tmp/waiting/"
#DIRECTION_SAVE_FILES = "../../waiting/"
THREAD_NUM = 5 #how many threads
global mylogger
gQueues = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)
gQueue_title = Queue.Queue(maxsize=20)
gMono_dict = {}
gTitle_dict = {}
_ucmq_timet = time.time()
_ucmq_cnt30sec_old = 100
_ucmq_cnt30sec_cnt = 0
_mono_time_sec = 10


"""CRITICAL>ERROR>WARNING>INFO>DEBUG>NOTSET
"""

def check_parser_ucmq_cmd(jstr):
    return 0, "abc"

def ucmq_put_msg_dict(dic, ucmq_url):
    global mylogger
    try:
        _test_data2 = {'name': 'userjpg', 'opt': 'put', 'ver': '2', 'data': json.dumps(dic)}
        _test_data_encode2 = urllib.urlencode(_test_data2)
        _ucmqIP = ucmq_url[ : ucmq_url.find('?')]
        res_data = urllib2.urlopen(_ucmqIP + "?" + _test_data_encode2)
        res = res_data.read()
        res_data.close()
        urllib.urlcleanup()
    except Exception, e:
        mylogger.info(str(e))
        pass

pic_sn = 0

def check_download_filename(jstr, cnt):
    global pic_sn, mylogger
    _dic1 = json.loads(jstr)
    if not "ip" in _dic1:
        return 0, "ip"
    if not "location" in _dic1:
        return 0, "location"
    if not "type_for" in _dic1:
        return 0, "type_for"
    if not "why" in _dic1:
        return 0, "why"
    if not "sn" in _dic1:
        return 0, "sn"
    if not "CMOS" in _dic1:
        return 0, "CMOS"

    pic_sn += 1
    _file_ext = _dic1["location"][_dic1["location"].rfind('.'):]
    localtime1 = time.localtime()
    _video_name = "%02d%02d%02d" % (localtime1.tm_hour, localtime1.tm_min, localtime1.tm_sec)
    _path2 = DIRECTION_SAVE_FILES + "%d_%s" % (int(time.time()),_video_name)# + _dic1["sn"]
    _path2 += "_G%d_E%d"%(_dic1["gain"],_dic1["exp"])
    try:
        if "Yval" in _dic1:
            _path2 += "_Y%d_U%d_V%d_%d"%(_dic1["Yval"],_dic1["Uval"],_dic1["Vval"],pic_sn) + _file_ext
        else:
            _path2 += "_%d"%(pic_sn) + _file_ext
    except Exception, e:
        mylogger.error(str(e))
    del _dic1
    return 1, _path2


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
        self.__timet = time.time()
        self.__downloadOKCnt = 0
        self.__downloadErrCnt = 0
        self.__logger = wtclib.create_logging('../log/downfilelog/thread%d.log' % idnum)
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret, Backup_ai_jpg, Backup_re_jpg

        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            _recv_dict = json.loads(_recv_json)
            self.__url_addr = "http://" + _recv_dict["ip"] + _recv_dict["location"]
            if time.time() - self.__timet > 30:
                self.__timet = time.time()
                self.__logger.info("sum=%d, ok=%d, err=%d in 30sec"
                                   %(self.__downloadOKCnt + self.__downloadErrCnt, self.__downloadOKCnt, self.__downloadErrCnt))
                self.__downloadOKCnt = 0
                self.__downloadErrCnt = 0

            self.__file_name = _recv_dict["path"]# + sec +".jpg"
            self.__logger.info(self.__url_addr+" as "+self.__file_name)
            #print "Child id=" + str(self.__id)+ str(time.time()) +"get url=" + str(self.__url_addr) +" save to " + str(self.__file_name)
            step = 1
            try:
                fd, info = urllib.urlretrieve(url=self.__url_addr, filename= self.__file_name)
            except Exception, e:
                step = -1
                ret_str = str(e)
                self.__logger.warning(str(e)+' '+self.__url_addr)
            finally:
                if step > 0:
                    if "content-length" in info.dict:
                        _ret_dic = {"ret": 1, "id": self.__id}
                        self.__downloadOKCnt += 1
                        if "plateGet" in _recv_dict and "LTy" in _recv_dict and "LTx" in _recv_dict and '1' == Backup_re_jpg:
                            _path, _file = os.path.split(str(_recv_dict["path"]))
                            localtime1 = time.localtime()
                            _day_str = "../../re/yuv/%d%02d%02d/" % (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
                            if not os.path.isdir(_day_str):
                                os.mkdir(_day_str)
                            _day_str += _recv_dict["sn"]
                            if not os.path.isdir(_day_str):
                                os.mkdir(_day_str)

                            _height = _recv_dict["RBy"] - _recv_dict["LTy"] + 1
                            _width = _recv_dict["RBx"] - _recv_dict["LTx"] + 1
                            _filen, _ext = os.path.splitext(_file)
                            _filename = "%d_%s_%dx%d.yuv"%(_recv_dict["plateGet"],_filen,_width,_height)
                            shutil.copy(_recv_dict["path"], os.path.join(_day_str, _filename))
                        if 'type_for' in _recv_dict and "place" == _recv_dict["type_for"] and '1' == Backup_ai_jpg:
                            localtime1 = time.localtime()
                            _day_str = '../../ai/jpg/%d%02d%02d/'% (localtime1.tm_year, localtime1.tm_mon, localtime1.tm_mday)
                            if not os.path.isdir(_day_str):
                                os.mkdir(_day_str)
                            _day_str += '%02d/'%(localtime1.tm_hour/4 * 4)
                            if not os.path.isdir(_day_str):
                                os.mkdir(_day_str)
                            _day_str += _recv_dict["sn"]
                            if not os.path.isdir(_day_str):
                                os.mkdir(_day_str)
                            _path, _filename = os.path.split(self.__file_name)
                            shutil.copy(_recv_dict["path"], os.path.join(_day_str, _filename))

                    else:
                        os.remove(self.__file_name)
                        self.__downloadErrCnt += 1
                        self.__logger.warning("no content-length, download " + self.__file_name +' from '+self.__url_addr+" failed")
                        _ret_dic = {"ret": "no content-length", "id": self.__id}

            #        gQueue_ret.put(json.dumps({"ret": 1, "id": self.__id, "filename":self.__file_name, "pic_type":_recv_dict["pic_type"]}))
                else:
                    _ret_dic = {"ret":ret_str, "id": self.__id}
            #        gQueue_ret.put(json.dumps({"ret": ret_str, "id": self.__id}))
                _recv_dict.update(_ret_dic)
                gQueue_ret.put(json.dumps(_recv_dict))
                #print "child end  id=" + str(self.__id) +" time="+ str(time.time())
                self.__logger.debug("child end  id=" + str(self.__id) +" time="+ str(time.time()))


class clear_tmp_waiting_files(threading.Thread):
    def __init__(self, idnum):
        self.__logger = wtclib.create_logging('../log/downfilelog/clear.log')
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret
        self.__logger.info("start running")
        while True:
            try:
                filenames = os.listdir(DIRECTION_SAVE_FILES)
                mylogger.info("remove waiting files")
                _many_files = len(filenames)
                if 0 != _many_files:
                    dir_sort = sorted(filenames)
                    _timeSec = int(time.time()) - 30
                    for i in range(_many_files):
                        if -1 == dir_sort[i].find('_'):
                            continue
                        _file_time = int(dir_sort[i][:dir_sort[i].find('_')])
                        if _file_time < _timeSec:
                            os.remove(os.path.join(DIRECTION_SAVE_FILES, dir_sort[i]))
                        else:
                            break

            except Exception, e:
                self.__logger.error(str(e))
            #finally:
            time.sleep(5)


"""update DB tables every 10 times or init"""
class add_db_titles(threading.Thread):
    def __init__(self, idnum):
        self.__logger = wtclib.create_logging('../log/downfilelog/title.log')
        threading.Thread.__init__(self)
    def run(self):
        global gQueue_title, gTitle_dict
        self.__logger.info("start running")
        title_cur = get_a_sql_cur_forever(self.__logger)
        while True:
            try:
                _recv_json = gQueue_title.get(block=True)
                _recv_dict = json.loads(_recv_json)
                _sql_str = 'json.loads'
                if not "sn" in _recv_dict:
                    continue
                if _recv_dict["sn"] in gTitle_dict:
                    _cnt = gTitle_dict[_recv_dict["sn"]] - 1
                    if _cnt <= 0 :
                        _cnt = 10
                else:
                    _cnt = 10
                gTitle_dict.update({_recv_dict["sn"] : _cnt})
                if 10 != _cnt: #not need update
                    continue

                _sql_str = 'update'

                _cmos1 = 0
                if "CMOS" in _recv_dict and type(_recv_dict["CMOS"]) == int:
                    _cmos1 = _recv_dict["CMOS"]

                _timetSec = int(time.time())
                _neighbor1 = ''
                if "neighbor" in _recv_dict:
                    _neighbor1 = _recv_dict["neighbor"]
                    if len(_neighbor1) < 10:
                        self.__logger.error("neighbor=%s is error" % _neighbor1)
                        _neighbor1 = ''

                _BTsn1 = ''
                if "bluetooth" in _recv_dict:
                    _BTsn1 = _recv_dict["bluetooth"]

                for i in range(1, 4):
                    _sql_str = "insert into SpaceStatusTable(Spaceid, cameraID, cmosID, CarportStatus)" \
                               "values('%s', '%s',0,0)ON DUPLICATE KEY UPDATE cmosID=0" \
                               "" % ((_recv_dict["sn"] + str(i)), _recv_dict["sn"])
                    title_cur.execute(_sql_str)
                    _sql_str = "insert into SpaceYUVFilterBuffTable(Spaceid, cameraID, cmosID, CarPos)" \
                               "values('%s', '%s',0, %d)ON DUPLICATE KEY UPDATE cmosID=0" \
                               "" % ((_recv_dict["sn"] + str(i)), _recv_dict["sn"], i - 1)
                    title_cur.execute(_sql_str)


                if '' == _neighbor1:
                    if 0 == title_cur.execute("select * from Equipment2cameraIdMem where equipmentID='%s'" % _recv_dict["sn"]):
                        _sql_str = "insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2,cmosID2" \
                                   ")values('%s', '%s',0, null,0)ON DUPLICATE KEY UPDATE cameraID2=null,cmosID2=0" \
                                   ""% (_recv_dict["sn"], _recv_dict["sn"])
                    title_cur.execute(_sql_str)

                    if 0 == title_cur.execute("select * from LampSettingTableMem where equipmentID='%s'" % _recv_dict["sn"]):
                        _sql_str = "insert into LampSettingTableMem(equipmentID, ReNewFlag, CtrlTableName, SpaceAll, " \
                                   "Space1ID, Space2ID, Space3ID, ManualCtrLampFlag)values('%s', 2, 'defaultXspace', 3, " \
                                   "'%s', '%s', '%s', 0)"% (_recv_dict["sn"], _recv_dict["sn"] + '1',
                                                            _recv_dict["sn"] + '2', _recv_dict["sn"] + '3')
                        title_cur.execute(_sql_str)
                    if 0 == title_cur.execute(
                                    "select * from hvpd2LampSettingTableMem where cameraID='%s' and cmosID=%d" % (
                                    _recv_dict["sn"], _cmos1)):
                        _sql_str = "insert into hvpd2LampSettingTableMem(cameraID,cmosID, ReNewFlag, Effect1EquipID)" \
                                   "values('%s', %d, 2, '%s')" % (_recv_dict["sn"], _cmos1, _recv_dict["sn"])
                        title_cur.execute(_sql_str)

                else:

                    _equipmentID = min(_recv_dict["sn"], _neighbor1)
                    _OtherID = max(_recv_dict["sn"], _neighbor1)
                    if len(_equipmentID) < 10:
                        self.__logger.error(
                            "EquipmentID=%s is error sn=%s neighbor=%s" % (_equipmentID, _recv_dict["sn"], _neighbor1))

                    if 0 == title_cur.execute(
                                    "select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=0" % _neighbor1):
                        _sql_str = "insert into OnlineHvpdStatusTableMem(cameraID, cmosID,LatestConnect,connectTimet," \
                                   "bluetooth,waiting_ex)values('%s',0,now(),%d,'Offline',0)" \
                                   "" % (_neighbor1, _timetSec - 3600)
                        title_cur.execute(_sql_str)

                    if 0 == title_cur.execute(
                                    "select * from Equipment2cameraIdMem where equipmentID='%s'" % _equipmentID):
                        _sql_str = "insert into Equipment2cameraIdMem(equipmentID, cameraID1, cmosID1, cameraID2, " \
                                   "cmosID2,ReNewFlag)values('%s', '%s', 0, '%s', 0, 2)"% (_equipmentID, _equipmentID, _OtherID)
                        title_cur.execute(_sql_str)
                    if 0 != title_cur.execute("select * from Equipment2cameraIdMem where equipmentID='%s'" % _OtherID):
                        _sql_str = "delete from Equipment2cameraIdMem where equipmentID='%s'" % _OtherID
                        title_cur.execute(_sql_str)
                    if 0 == title_cur.execute("select * from LampSettingTableMem where equipmentID='%s'" % _equipmentID):
                        _sql_str = "insert into LampSettingTableMem(equipmentID, ReNewFlag, CtrlTableName, SpaceAll," \
                                   "Space1ID,Space2ID, Space3ID, Space4ID, Space5ID, Space6ID, ManualCtrLampFlag)" \
                                   "values('%s', 2, 'defaultXspace', 6, '%s', '%s', '%s', '%s', '%s', '%s', 0)" \
                                   ""% (_equipmentID, _equipmentID + '1', _equipmentID + '2', _equipmentID + '3',
                                        _OtherID + '1',_OtherID + '2', _OtherID + '3')
                        title_cur.execute(_sql_str)

                    _sql_str = "select * from hvpd2LampSettingTableMem where cameraID='%s' and cmosID=%d"\
                               % (_recv_dict["sn"], _cmos1)
                    if 0 == title_cur.execute(_sql_str):
                        _sql_str = "insert into hvpd2LampSettingTableMem(cameraID, cmosID, ReNewFlag, Effect1EquipID)" \
                                   "values('%s', %d, 2, '%s')" % (_recv_dict["sn"], _cmos1, _equipmentID)
                        title_cur.execute(_sql_str)

            except Exception, e:
                self.__logger.error(str(e))
                self.__logger.error(_sql_str)
                if 'MySQL server has gone away' in str(e):
                    title_cur = get_a_sql_cur_forever(self.__logger)





def ucmq_put_msg(json_str, _ucmqIP):
    global mylogger
    try:
        _test_data2 = {'name': 'downloadmq', 'opt': 'put', 'ver': '2', 'data': json_str}
        _test_data_encode2 = urllib.urlencode(_test_data2)
        #_ucmqIP = ucmq_url[ : ucmq_url.find('?')]
        res_data = urllib2.urlopen(_ucmqIP + "?" + _test_data_encode2)
        res = res_data.read()
        res_data.close()
        urllib.urlcleanup()
        return 0, '0'
    except Exception, e:
        return -1, str(e)

class mono_dict_process(threading.Thread):
    def __init__(self, idnum):
        self.__logger = wtclib.create_logging('../log/downfilelog/mono.log')
        threading.Thread.__init__(self)
    def run(self):
        global gMono_dict, _mono_time_sec
        self.__logger.info("start running")
        (val, _ucmq_url) = wtclib.get_ucmq_url(None)
        print "ucmq=" + _ucmq_url
        if 0 == val:
            self.__logger.error("can not get ucmq url return " + _ucmq_url)
            os._exit()
        del val
        _ucmqIP = _ucmq_url[: _ucmq_url.find('?')]
        while True:

            _nowSec = int(time.time())
            try:
                _dic1 = gMono_dict.copy()
                for _key in _dic1:
                    if _nowSec - gMono_dict[_key][0] > _mono_time_sec:
                        ucmq_put_msg(gMono_dict[_key][1], _ucmqIP)
                        gMono_dict.pop(_key)
            except Exception, e:
                self.__logger.error(str(e))
            #finally:
            time.sleep(1)



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
                             passive=False, durable=False, auto_delete=False)
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
                             passive=False, durable=False, auto_delete=False)
    return channel


def get_a_sql_cur_forever(logger):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            logger.info(err)
            time.sleep(20)
    return _cur

def maybe_add_a_new_device(json_str, cur):
    global mylogger, gQueue_title, _mono_time_sec, _ucmq_cnt30sec_cnt, _ucmq_timet
    #print "json_str = %d"%len(json_str)
    _dic1 = json.loads(json_str)

    if not "ip" in _dic1:
        print "not ip in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return 0, 'no ip'


    if not "slave" in _dic1:
        print "not slace in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return 0, 'no slave'
    elif not type(_dic1["slave"])==int:
        print "not type slave is int" + " in line:" + str(sys._getframe().f_lineno)
        return 0, 'slave not int'

    if not "sn" in _dic1:
        print "not sn in _dic1"
        return 0, 'no sn'
    if len(_dic1["sn"]) < 10:
        mylogger.error("SN=%s is error" % _dic1["sn"])
        return 0, 'sn<10'

    if not "exp" in _dic1:
        print "not exp in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return 0, 'no exp'

    if not "gain" in _dic1:
        print "not gain in _dic1" + " in line:" + str(sys._getframe().f_lineno)
        return 0, 'no gain'


    _cmos = 0
    if "CMOS" in _dic1 and type(_dic1["CMOS"])==int:
        _cmos = _dic1["CMOS"]
    _b1 = time.time()
    _timetSec = int(time.time())
    _neighbor = ''
    if "neighbor" in _dic1:
        _neighbor = _dic1["neighbor"]
        if len(_neighbor) < 10:
            mylogger.error("neighbor=%s is error" % _neighbor)
            _neighbor = ''

    _BTsn = ''
    if "bluetooth" in _dic1:
        _BTsn = _dic1["bluetooth"]
    _MAC_addr = ''
    if "MAC" in _dic1:
        _MAC_addr = _dic1["MAC"]

    _pic_timeOut=0

    _timeSec = int(time.time())
    if _timeSec - _ucmq_timet > 30:
        _ucmq_timet = _timeSec
        if _ucmq_cnt30sec_cnt > 300:
            _mono_time_sec = 10
        elif _ucmq_cnt30sec_cnt < 200:
            _mono_time_sec -= 1
            if _mono_time_sec < 3:
                _mono_time_sec = 3
        _ucmq_cnt30sec_cnt = 0

    _ucmq_cnt30sec_cnt += 1
    try:
        gQueue_title.put_nowait(json_str)
        if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%((_dic1["sn"], _cmos))):
            cur.execute("insert into OnlineHvpdStatusTableMem(cameraID, cmosID, neighbor_camera, slave, ip, exp, gain, waiting_ex, bluetooth, "
                        "LatestConnect, connectTimet,last_pic_timet) values ('%s', %d, '%s', %d, '%s', %d, %d, 0,'%s', "
                        "now(), %d,%d)"
                        % (_dic1["sn"], _cmos, _neighbor, _dic1["slave"], _dic1["ip"],
                           _dic1["exp"], _dic1["gain"], _BTsn, _timetSec,_timetSec))


        else:
            _online = cur.fetchone()
            _a2 = cur.execute("select * from aisettingtablemem where cameraID='%s'"%_dic1["sn"])

            if _timeSec - _online[11] < 6 and "type_for" in _dic1 and "place" == _dic1["type_for"] \
                    and "location" in _dic1 and 0 != _a2:
                _pic_timeOut = 1
                mylogger.info("SN=%s is mono where now=%d, online=%d" %(_dic1["sn"], _timeSec, _online[11]) )

                _d1 = time.time()
                cur.execute("update OnlineHvpdStatusTableMem set neighbor_camera='%s', slave=%d, ip='%s',exp=%d,gain=%d,waiting_ex=%d, "
                        "bluetooth='%s',LatestConnect=now(),connectTimet=%d where cameraID='%s' and cmosID=%d"
                        % (_neighbor, _dic1["slave"], _dic1["ip"],_dic1["exp"], _dic1["gain"], (_online[12]+1)&3, _BTsn,_timetSec, _dic1["sn"], _cmos))


                if _dic1["sn"] in gMono_dict:
                    _timet = gMono_dict[_dic1["sn"]][0]
                else:
                    _timet = _timeSec
                gMono_dict.update({_dic1["sn"]:[_timet,json_str]})

            else:

                _sql = "update OnlineHvpdStatusTableMem set neighbor_camera='%s', slave=%d, ip='%s',exp=%d,gain=%d," \
                       "waiting_ex=%d, bluetooth='%s',connectTimet=%d,LatestConnect=now(),last_pic_timet=%d " \
                       "where cameraID='%s' and cmosID=%d"\
                       % (_neighbor, _dic1["slave"], _dic1["ip"], _dic1["exp"], _dic1["gain"], (_online[12]+1)&3, _BTsn, _timetSec,
                          _timetSec,_dic1["sn"], _cmos)

                cur.execute(_sql)
            if 0 == _a2:
                return 0, "no aisetting"
            if 0 != _pic_timeOut:
                return  0, 'mono'


        if "movedetect" in _dic1 and isinstance(_dic1["movedetect"],(str,unicode)) and 0 != int(_dic1["movedetect"]):
            if 0 != cur.execute("select CarCount,parking1State,parking2State,parking3State from aiouttable where "\
                                "cameraID='%s' and cmosID=%d"%(_dic1["sn"], _cmos)):
                _aiState = cur.fetchone()
                _video_type = ""
                if None != _aiState and None != _aiState[0]:
                    if _aiState[0] < 4 and _aiState[0] > 0:
                        _spaces = _aiState[0]
                    else:
                        _spaces = 3
                    for i in range(_spaces):
                        _video_type += '%d'%_aiState[1+i]
                else:
                    _video_type = "000"
                #if 0 != int(_dic1["movedetect"]):
                _sql_str = "select * from video_rtsp2mp4_table where cameraID='%s'"%_dic1["sn"]
                if 0 == cur.execute(_sql_str):
                    _sql_str = "insert into video_rtsp2mp4_table(cameraID,cmosID,movedetectTimet,startAIout)" \
                               "values('%s',0,%d,'%s')" % (_dic1["sn"], _timeSec, _video_type)
                    cur.execute(_sql_str)
                else:
                    _sql_str = "UPDATE video_rtsp2mp4_table SET startAIout='%s'" \
                               " WHERE cameraID='%s' and movedetectTimet=0"%(_video_type, _dic1["sn"])
                    cur.execute(_sql_str)
                    _sql_str = "UPDATE video_rtsp2mp4_table SET movedetectTimet=%d WHERE cameraID='%s'"%(_timeSec, _dic1["sn"])
                    cur.execute(_sql_str)


        a1 = cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d"%(_dic1["sn"], _cmos))
        return 1, cur.fetchmany(a1)[0]
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)
        return 0, str(e)

def HDCD_ucmq_cmd_process(jstr):
    return

def make_rabbitmq_msg(json_str, filename):
    _dic = json.loads(json_str)

    info = {"cam_id":_dic["sn"],"pic_full_name":filename,
            "Pic_type_for":_dic["why"], "CMOS":_dic["CMOS"],"time_now":int(time.time())}
    if "movedetect" in _dic:
        info.update({"movedetect":_dic["movedetect"]})
    return info

def make_PlateRabbitmq_msg(json_str):
    _dic = json.loads(json_str)

    info = {"cam_id":_dic["sn"],"pic_full_name":_dic["path"],
            "Pic_type_for":_dic["why"], "CMOS":_dic["CMOS"],
            "LTx":_dic["LTx"], "LTy":_dic["LTy"],
            "RBx":_dic["RBx"], "RBy":_dic["RBy"],
            "plateGet":_dic["plateGet"],"AIfile":_dic["AIfile"],"time_now":int(time.time())}

    return info

def Load_camera_table2Mem(cur):
    try:
        cur.execute("TRUNCATE TABLE OnlineHvpdStatusTableMem")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)


if __name__ == '__main__':

    if not os.path.isdir("../log/downfilelog"):
        try:
            os.mkdir("../log/downfilelog")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    #mylogger = create_logging("downfilelog/Mthread.log")
    mylogger = wtclib.create_logging("../log/downfilelog/Mthread.log")
    mylogger.info("start running")
    if not os.path.isdir('../../ai/jpg/'):
        try:
            os.mkdir('../../ai/jpg/')
        except Exception, e:
            mylogger.error(str(e))
            os._exit(2)
    if not os.path.isdir(DIRECTION_SAVE_FILES):
        try:
            os.mkdir(DIRECTION_SAVE_FILES)
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            mylogger.error(str(e))
            os._exit()

    (val, _ucmq_url) = wtclib.get_ucmq_url(None)
    print "ucmq="+_ucmq_url
    if 0 == val:
        mylogger.error("can not get ucmq url return "+ _ucmq_url)
        os._exit()
    del val

    Aimq = get_place_rabbitmq_channel()
    Remq = get_plate_rabbitmq_channel()
    if None == Aimq:
        mylogger.error("can get rabbitmq")
        os._exit()

    #mylogger.info(Aimq)
    #print Aimq
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"

    socket.setdefaulttimeout(10)
    j = 2000

    cur = get_a_sql_cur_forever(mylogger)
    if None == cur:
        mylogger.error("config fail with db")
        os._exit()
    #Load_camera_table2Mem(cur)
    #print time.time()
    _dic1 = wtclib.get_user_config_ret_dict("../conf/conf.conf", "file_save")
    if "backup_ai_jpg" in _dic1:
        Backup_ai_jpg = _dic1["backup_ai_jpg"]
    else:
        Backup_ai_jpg = '0'
    if "backup_re_jpg" in _dic1:
        Backup_re_jpg = _dic1["backup_re_jpg"]
    else:
        Backup_re_jpg = '0'
    del _dic1
    threads = []
    thread_idles = THREAD_NUM

    gThread_using_flag = []
    clear_tmp_waiting_files(1).start()
    mono_dict_process(2).start()
    add_db_titles(3).start()
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
    #Sqlite_cur, sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    try:
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "downloadpic" in _dic1:
            _version = _dic1["downloadpic"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
            del stat
        time.sleep(random.random())
        ServerID = wtclib.get_serverID()
        _sql_str = "insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, " \
                   "'python %s &', 180, %d,'%s')" % (_pid, __file__, time.time(), ServerID)
        cur.execute(_sql_str)
        _sql_str = "insert into AiSoftwareVersion(SoftwareName, version)values('downloadpic','%s')" \
                   "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version)
        cur.execute(_sql_str)
        del _dic1,_version
    except Exception, e:
        mylogger.error(str(e)+time.asctime())
        os._exit()
    _watchdogTime = int(sec_start)
    _sec_change = int(sec_start)
    _placemq_cnt = 0
    while True:
        _timeSecFloat = time.time()
        _timeSec = int(_timeSecFloat)
        if _timeSec - _watchdogTime > 30:
            _watchdogTime = _timeSec
            try:
                _sql_str = "update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'"%(_timeSec, _pid, ServerID)
                cur.execute(_sql_str)#wdi
            except Exception, e:
                mylogger.warning(str(e))
                if 'MySQL server has gone away' in str(e):
                    mylogger.error("cur.connection.open = %d" % (cur.connection.open))
                    cur = get_a_sql_cur_forever(mylogger)
        json_str = None
        _ucmq_loop = 12
        if thread_idles >= THREAD_NUM:
            thread_idles = THREAD_NUM#all thread is idle
            while True:
                json_str = ucmq_get_msg(_ucmq_url)
                if None != json_str:
                    break
                else:
                    time.sleep(0.1)
                    mylogger.debug("No ucmq sleep 0.1")
                _ucmq_loop -= 1
                if 0 == _ucmq_loop:
                    break
            sleep_sec = 0.015
            _queue_block = False
        elif 0 == thread_idles:   #all thread is busy
            _queue_block = True     #queue get block,until a thread is idle
        else:       #some thread is idle
            _queue_block = False
            json_str = ucmq_get_msg(_ucmq_url)

        _get_ucmq_time = time.time()

        mylogger.debug("thread_idle = %d"%thread_idles)
        if None != json_str:
            mylogger.info("ucmq: "+json_str)
            if isinstance(json_str, str):
                try:
                    json.loads(json_str, encoding='utf-8')
                except:
                    json_str = None
                    mylogger.warning("Not json:"+json_str)
        _add_a_device_time = 0.0
        _check_download_name_time = 0.0
        _get_mq_time = 0.0
        _send_rabitmq_time = 0.0
        if None != json_str:
            print "*********before add"
            _mysql_link_timet = time.time()
            _retV, sql_info = maybe_add_a_new_device(json_str, cur)
            _add_a_device_time = time.time()
            print "********after add"
            if 0 == _retV:
                mylogger.error("sql_info:%s,"%sql_info + json_str)
            else:
                print "*********before check"
                ret_val = check_download_filename(json_str, sql_info[7])
                _check_download_name_time = time.time()
                print "*********after check"
                if 1 == ret_val[0]:
                    _dic = json.loads(json_str)
                    _dict = {"path":ret_val[1]}
                    _dic.update(_dict)
                    print "*********before put queues"
                    for i in range(THREAD_NUM):
                        if gThread_using_flag[i] == 1:
                            gQueues[i].put_nowait(json.dumps(_dic))
                            gThread_using_flag[i] = 0
                            #print "Queue put to id%d"%i
                            mylogger.debug("Queue put to id%d"%i)
                            break
                    thread_idles -= 1
                    print "*********after put queues"
                    del _dict, _dic
                else:
                    mylogger.warning(ret_val[1])

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

        _get_mq_time = time.time()

        for rec_json in rec_json_buff:#

            dic1 = json.loads(rec_json)
            if not "ret" in dic1 or 1 != dic1["ret"] or not "type_for" in dic1:
                continue

            if "place" == dic1["type_for"]:
                msg = make_rabbitmq_msg(rec_json, dic1["path"])
                js_msg = json.dumps(msg)
                _place_rabbitmq_timet = _timeSec
                try:
                    mylogger.info("rabbitmq place: "+js_msg)
                    _place_rabbitmq_timet = _timeSec
                    Aimq.basic_publish(body=js_msg, exchange="place", properties=msg_props,
                                          routing_key="place queue")

                    _placemq_cnt += 1
                    _send_rabitmq_time = time.time()
                except Exception, e:
                    mylogger.debug(str(e))
                    mylogger.debug(Aimq)
                    Aimq = get_place_rabbitmq_channel()
                    #os._exit()
            elif "plate" == dic1["type_for"]:
                if not "plateGet" in dic1 or not "LTx" in dic1 or not "LTy" in dic1 or not "RBx" in dic1 \
                        or not "RBy" in dic1 or not "AIfile" in dic1:
                    continue

                msg = make_PlateRabbitmq_msg(rec_json)
                js_msg = json.dumps(msg)
                if dic1["LTx"] < 0 or dic1["LTy"] < 0 or dic1["RBx"] < 0 or dic1["RBy"] < 0:
                    mylogger.error(js_msg)
                    mylogger.error(rec_json)
                    continue
                mylogger.info("rabbitmq plate: " + js_msg)
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
        _curr_time = time.time()
        mylogger.debug("use %f second, and sleep %f"%(_curr_time-_timeSecFloat, sleep_sec))
        print "ucmqtime=%f,add=%f,check=%f,getmq=%f,rabbit=%f"%(_get_ucmq_time-_timeSecFloat,
                                                                _add_a_device_time - _get_ucmq_time,
                                                                _check_download_name_time - _add_a_device_time,
                                                                _get_mq_time - _check_download_name_time,
                                                                _curr_time-_send_rabitmq_time)

        if _sec_change != _timeSec:
            _sec_change = _timeSec
            print "placemq=%d"%_placemq_cnt
            if _placemq_cnt > 12:
                try:
                    _method, _header_f, _placemq_body = Aimq.basic_get("place.in")
                    if None != _method:
                        if _method.message_count > 5:
                            _rabbitmq_sleep = _method.message_count/9.1
                            print "sleep %f for %d RabbitMQs" % (_rabbitmq_sleep, _method.message_count)
                            time.sleep(_rabbitmq_sleep)
                except Exception, e:
                    mylogger.error(str(e))
                #ii = _rabbitmqCnt.
            _placemq_cnt = 0


        time.sleep(sleep_sec)

    print "exit ",time.time(), "start @", sec_start
    exit()