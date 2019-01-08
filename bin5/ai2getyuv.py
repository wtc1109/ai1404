import MySQLdb
import pika
import time,datetime
import json
import urllib
import urllib2
import os, sys
import requests
import wtclib
import ConfigParser
import socket

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur

def get_yuv_file_size(cur, camera, bay):
    global mylogger
    try:
        _sql = "select * from aiouttable_bay where cameraID='%s'and bay=%d and State=1" \
               % (camera, bay)
        if 0 == cur.execute(_sql):
            mylogger.info("0 = "+_sql)
            return None
        _ai_out = cur.fetchone()
        if None == _ai_out:
            mylogger.warning("%s aiout is none "%camera)
            return None
    except Exception, e:
        mylogger.error(str(e))
        mylogger.error(_sql)
        return None
    if 0 == max(_ai_out[14:18]):
        mylogger.warning("car position is all 0")
        return None
    if 0 == max(_ai_out[18:22]):#no plate
        _LTx = _ai_out[14]
        _LTy = _ai_out[15]
        _RBx = _ai_out[16]
        _RBy = _ai_out[17]

    elif 0 == max(_ai_out[22:26]):
        _LTx = _ai_out[18]
        _LTy = _ai_out[19]
        _RBx = _ai_out[20]
        _RBy = _ai_out[21]
    else:
        _LTx = min(_ai_out[18], _ai_out[22])
        _LTy = min(_ai_out[19], _ai_out[23])
        _RBx = max(_ai_out[20], _ai_out[24])
        _RBy = max(_ai_out[21], _ai_out[25])

    if (_RBy - _LTy + 1) * (_RBx - _LTx + 1) > 6000:
        _LTy = _RBy - 6000 / (_RBx - _LTx + 1)
    if _LTx == _RBx or _LTy == _RBy:
        mylogger.warning("LTx=%d, RBx=%d; LTy=%d, RBy=%d, can not use"%(_LTx,_RBx,_LTy,_RBy))
        return None
    if _LTx < 0:
        _LTx = 0
    if _LTy < 0:
        _LTy = 0
    _RBy += 1
    _RBx += 1
    if _RBx > 500:
        _RBx = 500
    if _RBy > 500:
        _RBy = 500
    if _RBy - _LTy > 225:
        _LTy = _RBy - 225
    _timeSec = int(time.time())
    try:
        _sql = "select * from spacestatustable where cameraID='%s' and cmosID=%d and bay=%d"%(_ai_out[0],_ai_out[1],_ai_out[2])
        if 0 == cur.execute(_sql):
            mylogger.warning("0 = "+_sql)
            return None
        _Old_plate_info = cur.fetchone()
        _diff_LTx = abs(_Old_plate_info[11] - _LTx)
        _diff_LTy = abs(_Old_plate_info[12] - _LTy)
        _diff_RBx = abs(_Old_plate_info[13] - _RBx)
        _diff_RBy = abs(_Old_plate_info[14] - _RBy)
        _diff_sec = abs(_Old_plate_info[15] - _timeSec)

        if _diff_LTx < 5 and _diff_LTy < 5 and _diff_RBx < 5 and _diff_RBy < 5 and _diff_sec < PLATE_INTERVAL_SECOND:
            mylogger.debug("too short time %d second for new yuv files"%_diff_sec)
            return None
        del _diff_sec, _diff_RBy, _diff_RBx, _diff_LTy, _diff_LTx, _Old_plate_info
        _sql = "update spacestatustable set plateLTx=%d, plateLTy=%d, plateRBx=%d, plateRBy=%d " \
               "where cameraID='%s' and bay=%d" % (_LTx, _LTy, _RBx, _RBy, camera, bay)
        cur.execute(_sql)
        #mylogger.debug(json.dumps({"plate%dget"%bay:500,"plate%dpos"%bay:"%d,%d;%d,%d"%(_LTx, _LTy, _RBx, _RBy)}))
        return {"plate%dget"%bay:500,"plate%dpos"%bay:"%d,%d;%d,%d"%(_LTx, _LTy, _RBx, _RBy)}
    except Exception, e:
        mylogger.error(str(e))
        mylogger.error(_sql)
        return  None

def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    global cur, mylogger,  PLATE_INTERVAL_SECOND,ServerID

    _timeSec = int(time.time())
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (_timeSec, os.getpid(),ServerID))
    except Exception, e:
        mylogger.error(str(e))
        if 1 != cur.connection.open:
            mylogger.error("cur.connection.open = %d" % (cur.connection.open))
            cur = get_a_sql_cur_forever(mylogger)
    #test = cur.execute("select * from ScreenConfigTable")
    _dic_info = json.loads(body)
    if "quit" in _dic_info:
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()

    mylogger.debug("msg recv " + body)
    if not "sn" in _dic_info:
        mylogger.debug("not sn in _dic")
        return


    try:
        _sql = "select ip from OnlineHvpdStatusTableMem where cameraID='%s'"% (_dic_info["sn"])
        if 0 == cur.execute(_sql):
            mylogger.warning("cameraID='%s' and cmosID=%d is not online" % (_dic_info["sn"], _dic_info["CMOS"]))
            return
        (_cameraIp,) = cur.fetchone()
        if None == _cameraIp:
            mylogger.warning("%s ip is none"%_dic_info["sn"])
            return
        _sql = "select bays from aisettingtable_camera_mem where cameraID='%s'"%_dic_info["sn"]
        if 0 == cur.execute(_sql):
            mylogger.warning("%s get bays None" % _dic_info["sn"])
        _bays, = cur.fetchone()
        if None == _bays:
            mylogger.warning("%s get bays None2" % _dic_info["sn"])
    except Exception, e:
        mylogger.error(str(e))
        mylogger.error(_sql)
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)
        return
    _ret_dict = {}
    for i in range(_bays):
        _yuv_size = get_yuv_file_size(cur, _dic_info["sn"], i+1)
        if None != _yuv_size:
            _ret_dict.update(_yuv_size)
    if len(_ret_dict) < 1:
        return
    try:
        _sql = "select pic_full_name from aiouttable_camera where cameraID='%s' and cmosID=0"%(_dic_info["sn"])
        if 0 != cur.execute(_sql):
            (_ai_file,) = cur.fetchone()

        if None == _ai_file:
            mylogger.debug("AIfile is None")
            _ai_file = "/1.jpg"
    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(_sql)
        return
        #_dic_pos = {}
    #mylogger.debug(json.dumps(_ret_dict))
    try:
        AIfile = _ai_file[_ai_file.rfind('/')+1:]

        _ret_dict.update({"AIfile":AIfile})
        #mylogger.debug(json.dumps(_ret_dict))

        mylogger.info(json.dumps(_ret_dict) + " to %s"%_dic_info["sn"])
        _ret,_err = wtclib.http_get_cgi_msg2device(dict_msg=_ret_dict, ip=_cameraIp, cgi_name="setting")
        if 1 != _ret:
            mylogger.warning("get msg2device = %s"%_err)
        else:
            try:
                _sql = "update spacestatustable set plate_RenewTime=%d,YUVGetfilesTime=%d" \
                       " where cameraID='%s'" % (_timeSec, _timeSec, _dic_info["sn"])
                cur.execute(_sql)
            except Exception, e:
                mylogger.error(str(e))
                mylogger.error(_sql)
    except Exception,e:
        mylogger.error(str(e))
    return


if __name__ == '__main__':
    global mylogger
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/airet/ai2getyuv.log")
    mylogger.info("start running")
    cur = get_a_sql_cur_forever(mylogger)
    ServerID = wtclib.get_serverID()
    #sqlite3_cur, sqlite3_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 35, %d,'%s')" % (os.getpid(), __file__, time.time(),ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "ai2getyuv" in _dic1:
            _version = _dic1["ai2getyuv"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai2getyuv','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
        os._exit()

    socket.setdefaulttimeout(2)

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "rabbitmq")

    if "aioutmq_server_addr" in conf_dict:
        _mq_host = conf_dict["aioutmq_server_addr"]
    else:
        _mq_host = wtclib.get_ip_addr1("eth0")
    if "aioutmq_server_port" in conf_dict:
        _mq_port = int(conf_dict["aioutmq_server_port"])
    else:
        _mq_port = 5672
    if "aioutmq_exchange" in conf_dict:
        _mq_exchange = conf_dict["aioutmq_exchange"]
    else:
        _mq_exchange = "AiOut.tr"
    if "aioutmq_user_name" in conf_dict:
        _mq_user_name = conf_dict["aioutmq_user_name"]
    else:
        _mq_user_name = "user1"
    if "aioutmq_passwd" in conf_dict:
        _mq_passwd = conf_dict["aioutmq_passwd"]
    else:
        _mq_passwd = "9876543"
    if "aioutmq_vhost" in conf_dict:
        _mq_vhost = conf_dict["aioutmq_vhost"]
    else:
        _mq_vhost = "OutTrig"

    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "plate")
    PLATE_INTERVAL_SECOND = 300
    if "interval_sec" in conf_dict:
        PLATE_INTERVAL_SECOND = int(conf_dict["interval_sec"])
    if PLATE_INTERVAL_SECOND > 600 or PLATE_INTERVAL_SECOND < 5:
        PLATE_INTERVAL_SECOND = 300



    while True:
        while True:
            try:
                credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
                conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials)
                conn_broker = pika.BlockingConnection(conn_params)
                break
            except Exception, e:
                mylogger.info(str(e))
                time.sleep(20)
        while True:
            try:
                channel = conn_broker.channel()

                #channel.exchange_declare(exchange="AiOut",exchange_type="fanout", passive=False, durable=False, auto_delete=True)
                channel.queue_declare(queue="ai2getyuv")
                channel.queue_bind(queue="ai2getyuv", exchange="AiOut.yuvfilter")
                break
            except Exception, e:
                mylogger.info(str(e))
                time.sleep(20)


        try:
            channel.basic_consume(msg_consumer, queue="ai2getyuv", consumer_tag="getyuv")
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))