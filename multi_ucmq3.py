import ConfigParser
import Queue
import json
import math
import os
import socket
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
THREAD_NUM = 1 #how many threads
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

def check_download_filename(jstr, ucmq_url):
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
    sec = "%d_%d" % (int(inter1), int(1000 * fraction1))
    del fl, fraction1, inter1
    _path = _top_top + '/waiting/' + _dic1["sn"] +'/' + sec + ".jpg"
    if "place" == _dic1["type_for"]:
        ucmq_put_msg(_dic1, ucmq_url)

    return 1, _path




def ucmq_get_msg(ucmq_url):

    while True:
        while True:
            try:
                res_data = urllib2.urlopen(ucmq_url)
                break
            except urllib2.URLError, e:
                print e
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
                    try:
                        length = info.dict["content-length"]  # if length is 0,so remove the empty file
                    except KeyError:
                        os.remove(self.__file_name)
                        self.__logger.warning("no content-length, download " + self.__file_name +" failed")
                    _ret_dic = {"ret":1, "id": self.__id, "file":self.__file_name}

            #        gQueue_ret.put(json.dumps({"ret": 1, "id": self.__id, "filename":self.__file_name, "pic_type":_recv_dict["pic_type"]}))
                else:
                    _ret_dic = {"ret":ret_str, "id": self.__id}
            #        gQueue_ret.put(json.dumps({"ret": ret_str, "id": self.__id}))
                _recv_dict.update(_ret_dic)
                gQueue_ret.put(json.dumps(_recv_dict))
                #print "child end  id=" + str(self.__id) +" time="+ str(time.time())
                self.__logger.debug("child end  id=" + str(self.__id) +" time="+ str(time.time()))


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
                                 passive=False, durable=False, auto_delete=True)
            _Plate_channel = conn_broker.channel()
            _Plate_channel.exchange_declare(exchange=Rabbitmq_Plate_exchange, exchange_type=_Plate_exchange_type,
                                            passive=False, durable=False, auto_delete=True)
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
        return
    if not "slave" in _dic1:
        return
    if not "sn" in _dic1:
        return
    a1 = cur.execute("select * from AiSettingTable where sn='"+_dic1["sn"]+"'")
    if 0 == a1:
        str_info = "insert into AiSettingTable (sn, ip, slave_flag, user_set_space," \
                   "installation_space, valid_space_bitmap, LedCtrl_bitmap_sn," \
                   "LedCtrl_Selected_auto_menu, ParkingLine_auto_manual_flag) values" \
                   "('%s', '%s', %d, 3, 3, 7, '%s', 0, 0)" \
                   % (_dic1["sn"], _dic1["ip"], _dic1["slave"], _dic1["sn"])
        cur.execute(str_info)
        str_info = ''
        if "neighbor" in _dic1:
            str_info = "neighbor_sn='%s'"%_dic1["neighbor"]
        if "bluetooth_id" in _dic1:
            if 0 == len(str_info):
                str_info = "bluetooth_id='%s'" % _dic1["bluetooth_id"]
            else:
                str_info += ", bluetooth_id='%s'" % _dic1["bluetooth_id"]
        if 0 != len(str_info):
            _update = "update AiSettingTable set " + str_info
            _update += " where sn=%s" %_dic1["sn"]
            cur.execute(_update)

    else:
        a1info = cur.fetchmany(a1)
        if (_dic1["ip"] != a1info[0][1]) or (_dic1["slave"] != a1info[0][2]):
            str_info = "update AiSettingTable set ip='%s', slave_flag=%d"%(_dic1["ip"], _dic1["slave"])
            if "neighbor" in _dic1:
                str_info += ", neighbor_sn='%s'"%_dic1["neighbor"]
            if "bluetooth_id" in _dic1:
                str_info += ", bluetooth_id='%s'"%_dic1["bluetooth_id"]
            str_info += " where sn='%s'"%_dic1["sn"]
            cur.execute(str_info)

    a1 = cur.execute("select * from AiSettingTable where sn='" + _dic1["sn"] + "'")
    return cur.fetchmany(a1)[0]

def HDCD_ucmq_cmd_process(jstr):
    return

def make_rabbitmq_msg(json_str, filename, sql):
    _dic = json.loads(json_str)

    try:
        why = _dic["why"]
        info = {"cam_id":_dic["sn"],"pic_full_name":filename,
                "slot_count":sql[5], "is_manual":sql[13],
                "slot_region1":sql[16],"slot_region2":sql[17],
                "slot_region3": sql[18],
                "slot_install":sql[6],
                "slot_bitmap":sql[7], "Pic_type_for":_dic["why"]}
    except:
        info = {"cam_id": _dic["sn"], "pic_full_name": filename,
                "slot_count": sql[5], "is_manual": sql[13],
                "slot_region1": sql[16], "slot_region2": sql[17],
                "slot_region3": sql[18],
                "slot_install": sql[6],
                "slot_bitmap": sql[7]}

    return info



if __name__ == '__main__':
    global mylogger
    if not os.path.isdir("../log/downfilelog"):
        try:
            os.mkdir("../log/downfilelog")
        except Exception, e:
            print e
            os._exit()
    #mylogger = create_logging("downfilelog/Mthread.log")
    mylogger = wtclib.create_logging("../log/downfilelog/Mthread.log")
    mylogger.info("start running")
    if not os.path.isdir(DIRECTION_SAVE_FILES):
        try:
            os.mkdir(DIRECTION_SAVE_FILES)
        except Exception, e:
            print e
            mylogger.error(str(e))
            os._exit()

    (val, _ucmq_url) = wtclib.get_ucmq_url(None)
    if 0 == val:
        mylogger.error("can not get ucmq url return "+ _ucmq_url)
        os._exit()
    del val
    (Aimq, Remq) = get_a_rabbitmq_channel()
    if None == Aimq:
        mylogger.error("can get rabbitmq")
        os._exit()


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
    j = 50

    cur = get_a_sql_cur()
    if None == cur:
        mylogger.error("config fail with db")
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
    while j > 0:
        json_str = None
        if thread_idles >= THREAD_NUM:
            thread_idles = THREAD_NUM#all thread is idle
            while True:
                json_str = ucmq_get_msg(_ucmq_url)
                if None != json_str:
                    break
                else:
                    time.sleep(0.5)
            sleep_sec = 0.02
            _queue_block = False
        elif 0 == thread_idles:   #all thread is busy
            _queue_block = True     #queue get block,until a thread is idle
        else:       #some thread is idle
            _queue_block = False
            json_str = ucmq_get_msg()
            #sleep_sec = (THREAD_NUM - thread_idles)/(2.0*THREAD_NUM)
        #print "thread_idle = %d"%thread_idles
        mylogger.debug("thread_idle = %d"%thread_idles)
        if isinstance(json_str, str):
            try:
                json.loads(json_str, encoding='utf-8')
            except:
                json_str = None
        if None != json_str:
            sql_info = maybe_add_a_new_device(json_str, cur)
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
                mylogger.debug("Queue get blocked")
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

        for rec_json in rec_json_buff:
            dic1 = json.loads(rec_json)
            if not "ret" in dic1:
                continue
            if 1 != dic1["ret"]:
                continue
            if not "file" in dic1:
                continue
            if not "type_for" in dic1:
                continue
            if "place" == dic1["type_for"]:
                msg = make_rabbitmq_msg(rec_json, dic1["file"], sql_info)
                js_msg = json.dumps(msg)
                Aimq.basic_publish(body=js_msg, exchange=Rabbitmq_Place_exchange, properties=msg_props,
                                      routing_key=Rabbitmq_Place_router_key)
            elif "plate" == dic1["type_for"]:
                msg = make_rabbitmq_msg(rec_json, dic1["file"], sql_info)
                js_msg = json.dumps(msg)
                Remq.basic_publish(body=js_msg, exchange=Rabbitmq_Plate_exchange, properties=msg_props,
                                      routing_key=Rabbitmq_Plate_router_key)
            del dic1
        time.sleep(sleep_sec)
        #print "sleep ",sleep_sec
        mylogger.debug("sleep %f"%sleep_sec)

        j -= 1
    print "exit ",time.time(), "start @", sec_start
    exit()