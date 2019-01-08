import MySQLdb
import pika
import time,datetime
import json
import urllib
import urllib2
import os, sys
import requests
import wtclib
import random
import socket

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur


def get_yuv_file_size(cur, camera, bay):
    try:
        a1 = cur.execute("select * from AiOutTable where cameraID='%s'" % camera)
        if 0 == a1:
            mylogger.warning(
                "0 == select * from AiOutTable where cameraID='%s'" % camera)
            return None
        _ai_out = cur.fetchone()
        if None == _ai_out:
            mylogger.warning("aiout is none")
            return None
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)
        return None
    if 0 == _ai_out[4+bay]:
        mylogger.debug("%s parking%d State=0"%(camera, bay))
        return None
    _carNo = bay-1
    if 0 == max(_ai_out[50+8*_carNo], _ai_out[51+8*_carNo],
                _ai_out[52+8*_carNo], _ai_out[53+8*_carNo]):#no plate
        _LTx = _ai_out[38+4*_carNo]
        _LTy = _ai_out[39 + 4 * _carNo]
        _RBx = _ai_out[40 + 4 * _carNo]
        _RBy = _ai_out[41 + 4 * _carNo]
    elif 0 == max(_ai_out[54+8*_carNo], _ai_out[55+8*_carNo],
                _ai_out[56+8*_carNo], _ai_out[57+8*_carNo]):
        _LTx = _ai_out[50 + 8 * _carNo]
        _LTy = _ai_out[51 + 8 * _carNo]
        _RBx = _ai_out[52 + 8 * _carNo]
        _RBy = _ai_out[53 + 8 * _carNo]
    else:
        _LTx = min(_ai_out[50 + 8 * _carNo], _ai_out[54 + 8 * _carNo])
        _LTy = min(_ai_out[51 + 8 * _carNo], _ai_out[55 + 8 * _carNo])
        _RBx = max(_ai_out[52 + 8 * _carNo], _ai_out[56 + 8 * _carNo])
        _RBy = max(_ai_out[53 + 8 * _carNo], _ai_out[57 + 8 * _carNo])
    if 0 == max(_LTx, _LTy, _RBx, _RBy):
        #mylogger.debug("lTx=0")
        return None
    if (_RBy - _LTy + 1) * (_RBx - _LTx + 1) > 10000:
        _LTy = _RBy - 10000 / (_RBx - _LTx + 1)

    if _LTx == _RBx or _LTy == _RBy:
        mylogger.warning("LTx=%d, RBx=%d; LTy=%d, RBy=%d, can not use"%(_LTx,_RBx,_LTy,_RBy))
        return None
    _LTx -= 3
    _LTy -= 3
    if _LTx < 0:
        _LTx = 0
    if _LTy < 0:
        _LTy = 0
    _RBy += 3
    _RBx += 3
    if _RBx > 500:
        _RBx = 500
    if _RBy > 500:
        _RBy = 500

    _timeSec = int(time.time())
    try:
        if 0 == cur.execute("select * from SpaceForReInfoTable where Spaceid='%s%d'" % (camera, bay)):
            cur.execute("insert into SpaceForReInfoTable(Spaceid)values('%s%d')" % (camera, bay))
        cur.execute("select * from SpaceForReInfoTable where Spaceid='%s%d'" % (camera, bay))
        _Old_plate_info = cur.fetchone()
        if None != _Old_plate_info:
            _diff_LTx = abs(_Old_plate_info[1] - _LTx)
            _diff_LTy = abs(_Old_plate_info[2] - _LTy)
            _diff_RBx = abs(_Old_plate_info[3] - _RBx)
            _diff_RBy = abs(_Old_plate_info[4] - _RBy)
            _diff_sec = abs(_Old_plate_info[5] - _timeSec)
            if _diff_LTx < 5 and _diff_LTy < 5 and _diff_RBx < 5 and _diff_RBy < 5 and _diff_sec < PLATE_INTERVAL_SECOND:
                mylogger.debug("too short time %d second for new yuv files" % _diff_sec)
                return None
        cur.execute(
            "update SpaceForReInfoTable set plateLTx=%d, plateLTy=%d, plateRBx=%d, plateRBy=%d where "
            "Spaceid='%s%d'" % (_LTx, _LTy, _RBx, _RBy, camera, bay))
        return {"plate%dpos"%bay:"%d,%d;%d,%d"%(_LTx, _LTy, _RBx, _RBy),"plate%dget"%bay:500}
    except Exception, e:
        mylogger.error(str(e))
        return None


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    global cur, mylogger,  PLATE_INTERVAL_SECOND,ServerID

    _timeSec = int(time.time())
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (_timeSec, os.getpid(),ServerID))
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
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
        _sql_str = "select Slot_count from aisettingtablemem where cameraID='%s'"%_dic_info["sn"]
        if 0 == cur.execute(_sql_str):
            return
        _bays, = cur.fetchone()
        if None == _bays:
            return
        if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s'" % (
                _dic_info["sn"])):
            mylogger.warning("cameraID='%s' is not online" % (_dic_info["sn"]))
            return
        _cameraInfo = cur.fetchone()
        if None == _cameraInfo:
            mylogger.warning("online info is none")
            return
    except Exception, e:
        mylogger.error(str(e))
        return

    _ret_dict = {}
    _yuv = []
    for i in range(_bays):

        _ret = get_yuv_file_size(cur, _dic_info["sn"], i+1)
        if None == _ret:
            _yuv.append(0)
            #mylogger.debug("Get %s %d None" % (_dic_info["sn"], i + 1))
            continue
        else:
            _ret_dict.update(_ret)
            _yuv.append(1)
            #mylogger.debug("Get %s %d=%s" % (_dic_info["sn"], i + 1, json.dumps(_ret)))
    if len(_ret_dict) < 1:
        mylogger.info("None need yuv file with "+_dic_info["sn"])
        return
    try:
        _sql_str = "select pic_full_name from aiouttable where cameraID='%s'"%_dic_info["sn"]
        if 0 == cur.execute(_sql_str):
            mylogger.info("0= "+_sql_str)
            return
        _ai_file, = cur.fetchone()
        if None == _ai_file:
            _ai_file= '/1.jpg'
        AIfile = _ai_file[_ai_file.rfind('/')+1:]
        _ret_dict.update({"AIfile":AIfile})

        mylogger.info(json.dumps(_ret_dict) + " to %s ip:%s"%(_dic_info["sn"], _cameraInfo[4]))
        _ret,_err = wtclib.http_get_cgi_msg2device(dict_msg=_ret_dict, ip=_cameraInfo[4], cgi_name="setting")
        if 1 != _ret:
            mylogger.warning("get msg2device = %s"%_err)
        else:
            for i in range(_bays):
                if 0 == _yuv[i]:
                    continue
                cur.execute("update SpaceForReInfoTable set RenewTime=%d where "
                            "Spaceid='%s%d'"%(_timeSec, _dic_info["sn"], i))

    except Exception, e:
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


    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 35, %d,'%s')" % (os.getpid(), __file__, (time.time()),ServerID))
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
    if "interval_sec" in conf_dict:
        PLATE_INTERVAL_SECOND = int(conf_dict["interval_sec"])
        if PLATE_INTERVAL_SECOND > 600 or PLATE_INTERVAL_SECOND < 5:
            PLATE_INTERVAL_SECOND = 60
    else:
        PLATE_INTERVAL_SECOND = 60

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