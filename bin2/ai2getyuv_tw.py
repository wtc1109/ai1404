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
    if not "place" in _dic_info:
        mylogger.warning("not place in _dic")
        return
    if not "space" in _dic_info:
        mylogger.warning("not space in _dic")
        return
    _carNo = _dic_info["place"]
    _cmos = 0
    if "CMOS" in _dic_info and type(_dic_info["CMOS"])==int:
        _cmos = _dic_info["CMOS"]

    try:
        a1 = cur.execute("select * from AiOutTable where cameraID='%s' and cmosID=%d" % (_dic_info["sn"], _cmos))
        if 0 == a1:
            mylogger.warning(
                "0 == select * from AiOutTable where cameraID='%s' and cmosID=%d" % (_dic_info["sn"], _cmos))
            return
        _ai_out = cur.fetchone()
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)
        return
    if 0 == _ai_out[5+_carNo]:
        mylogger.warning("parking%d State=0"%(_carNo+1))
        return
    _hvpd = _dic_info["sn"]

    try:
        if 0 == cur.execute("select * from OnlineHvpdStatusTableMem where cameraID='%s' and cmosID=%d" % (
        _hvpd, _dic_info["CMOS"])):
            mylogger.warning("cameraID='%s' and cmosID=%d is not online" % (_hvpd, _dic_info["CMOS"]))
            return
        _cameraInfo = cur.fetchone()
        if None == _cameraInfo:
            mylogger.warning("get online information none")
            return
        if None == _cameraInfo[4]:
            mylogger.warning("ip is none")
            return
    except Exception, e:
        mylogger.error(str(e))
        return
    if 0 == _dic_info["CMOS"]:
        _car = _carNo + 1
    else:
        _car = _carNo + 4

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

    if (_RBy - _LTy + 1) * (_RBx - _LTx + 1) > 6000:
        _LTy = _RBy - 6000 / (_RBx - _LTx + 1)

    if _LTx == _RBx or _LTy == _RBy:
        mylogger.warning("LTx=%d, RBx=%d; LTy=%d, RBy=%d, can not use"%(_LTx,_RBx,_LTy,_RBy))
        return
    _LTx /= 5
    _LTy /= 5
    _RBy /= 5
    _RBx /= 5
    #_LTy -= 1
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
    if _RBy - _LTy > 125:
        _LTy = _RBy - 125
    try:
        if 0 == cur.execute("select * from SpaceForReInfoTable where Spaceid='%s'"%_dic_info["space"]):
            cur.execute("insert into SpaceForReInfoTable(Spaceid)values('%s')"%_dic_info["space"])
        cur.execute("select * from SpaceForReInfoTable where Spaceid='%s'"%_dic_info["space"])
        _Old_plate_info = cur.fetchone()
        if None != _Old_plate_info:
            _diff_LTx = abs(_Old_plate_info[1] - _LTx)
            _diff_LTy = abs(_Old_plate_info[2] - _LTy)
            _diff_RBx = abs(_Old_plate_info[3] - _RBx)
            _diff_RBy = abs(_Old_plate_info[4] - _RBy)
            _diff_sec = abs(_Old_plate_info[5] - _timeSec)
            if _diff_LTx < 5 and _diff_LTy < 5 and _diff_RBx < 5 and _diff_RBy < 5 and _diff_sec < PLATE_INTERVAL_SECOND:
                mylogger.debug("too short time %d second for new yuv files"%_diff_sec)
                return
    except Exception, e:
        mylogger.error(str(e))
        return
    try:
        #_dic_msg = {"plate%dpos"%_car:"%d,%d;%d,%d"%(_LTx, _LTy, _RBx, _RBy),"plate%dget"%_car:500}
        AIfile = _ai_out[2][_ai_out[2].rfind('/')+1:]
        _dic_msg = {"plate%dpos"%_car:"%d,%d;%d,%d"%(_LTx, _LTy, _RBx, _RBy),"plate%dget"%_car:55,"AIfile":AIfile}
        #_dic_msg.update(_dic_pos)
        mylogger.info(json.dumps(_dic_msg) + " to %s"%_dic_info["sn"])
        _ret,_err = wtclib.http_get_cgi_msg2device(dict_msg=_dic_msg, ip=_cameraInfo[4], cgi_name="setting")
        if 1 != _ret:
            mylogger.warning("get msg2device = "+ _err)
        else:
            try:
                cur.execute("update SpaceForReInfoTable set plateLTx=%d, plateLTy=%d, plateRBx=%d, plateRBy=%d, RenewTime=%d where "
                            "Spaceid='%s'"%(_LTx, _LTy, _RBx, _RBy, _timeSec, _dic_info["space"]))
            except Exception, e:
                mylogger.error(str(e))
    except Exception,e:
        mylogger.error(str(e))
        mylogger.error("ip is %s"%_cameraInfo[4])
        mylogger.error()
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
                mylogger.error(str(e))
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

        mylogger.error("consume end")