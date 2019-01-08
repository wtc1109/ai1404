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

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur



def wdi(cur):
    global mylogger,ServerID
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(), ServerID))
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)


def msg_consumer(channel, method, header, body):
    global cur, mylogger, channelOut, msg_props, interval_sec

    channel.basic_ack(delivery_tag=method.delivery_tag)
    _timeSec = int(time.time())
    wdi(cur)
    mylogger.debug("msg recv" + body)
    try:
        _dic_info = json.loads(body)
    except Exception, e:
        mylogger.warning(str(e))
        mylogger.warning("len=%d"%len(body))
        mylogger.warning("msg="+body)
        return
    if "quit" in _dic_info:
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()
        mylogger.debug("quit")
    mylogger.debug(body)
    if "aimsg" in _dic_info:
        try:
            cur.execute("update aisoftwareversion set warning='%s' where SoftwareName='ai'"%_dic_info["aimsg"])
        except Exception,e:
            mylogger.error(str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylogger)
        finally:
            return
    if not "cam_id" in _dic_info:
        mylogger.debug("not cam_id in _dic_info")
        try:
            mylogger.debug("basic_publish:" + body + " @ %d" % _timeSec)
            channelOut.basic_publish(body=body, exchange="AiOut.filter", properties=msg_props, routing_key="hola")
        except Exception, e:
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()
            mylogger.error("channelOut Error " + str(e))
        return
    if not "CMOS" in _dic_info:
        mylogger.debug("not CMOS in _dic_info")
        return
    if not type(_dic_info["CMOS"])==int:
        mylogger.debug("not type CMOS is int")
        return
    _cmos = _dic_info["CMOS"]

    _sql_str = "select * from AiOutTable where cameraID='%s' and cmosID=%d"%(_dic_info["cam_id"], _cmos)
    try:
        if 0 == cur.execute(_sql_str):
            mylogger.debug("None= "+_sql_str)
            return
        _ai_out = cur.fetchone()
        if None == _ai_out:
            mylogger.warning("%s aiout is none"%_dic_info["cam_id"])
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)


    _hvpd = _dic_info["cam_id"]
    if 1 == _cmos:
        _offset = 4
    else:
        _offset = 1

    try:
        _need_rabbitmq = 0
        _sql_str = 'init'
        _bay_change = []
        for i in range(_ai_out[4],3):
            _spaceid = _hvpd + str(i + _offset)
            cur.execute("update SpaceStatusTable set CarportStatus=128, RenewTime=0 where Spaceid='%s'"
                        % (_spaceid))
        for i in range(_ai_out[4]):
            _spaceid = _hvpd+str(i+_offset)
            try:
                _sql_str = "select CarportStatus from SpaceStatusTable where Spaceid='%s'"%_spaceid
                cur.execute(_sql_str)
                (_space_for,) = cur.fetchone()
                if None == _space_for:
                    mylogger.warning("%s status is none"%(_spaceid))
                    continue
            except Exception, e:
                mylogger.error(_sql_str+str(e))
                continue

            if _ai_out[5 + i] != 1 and 0 != _ai_out[5 + i]:
                continue
            cur.execute("update SpaceStatusTable set CarportStatus=%d, RenewTime=%d where Spaceid='%s'"
                        % (_ai_out[5 + i], _timeSec, _spaceid))
            if 1 == _ai_out[5 + i]:  #need get yuv files
                _sql_str = "update SpaceYUVFilterBuffTable set SpaceRenewTime=0,YUVRenewTime=%d where " \
                           "Spaceid='%s' and YUVRenewTime=0" % (_timeSec, _spaceid)
                cur.execute(_sql_str)
            if _space_for != _ai_out[5 + i]:
                _need_rabbitmq = 1  #status change, need mq to change lamp
                _bay_change.append(i)
                if 0 == _ai_out[5 + i]:
                    _sql_str = "update SpaceStatusTable set parkout_timet=%d,parkout_time=now() where Spaceid='%s'" % (
                        _timeSec, _spaceid)
                else:
                    _sql_str = "update SpaceStatusTable set parkin_timet=%d,parkin_time=now() where Spaceid='%s'" % (
                        _timeSec, _spaceid)

                cur.execute(_sql_str)


        if 0 != _need_rabbitmq:
            msg = json.dumps({"sn": _hvpd, "CMOS": _cmos})
            if len(_bay_change) > 0:
                _sql_str = "select ServerID,startAIout from video_rtsp2mp4_table where cameraID='%s'" % _dic_info[
                    "cam_id"]
                if 0 != cur.execute(_sql_str):
                    _video_table = cur.fetchone()
                    if None != _video_table[0]:
                        _startAIout = ''
                        for i in range(_ai_out[4]):
                            if i in _bay_change:
                                _startAIout += '4'
                            else:
                                _startAIout += _video_table[1][i]

                        _sql_str = "update video_rtsp2mp4_table set startAIout='%s' where cameraID='%s'" \
                                   "" % (_startAIout, _dic_info["cam_id"])
                        cur.execute(_sql_str)
            try:
                mylogger.debug("basic_publish:"+msg+" @ %d"%_timeSec)
                channelOut.basic_publish(body=msg, exchange="AiOut.filter", properties=msg_props,routing_key="hola")
            except Exception, e:
                channel.basic_cancel(consumer_tag="hello-consumer2")
                channel.stop_consuming()
                mylogger.error("channelOut Error "+str(e))

    except Exception, e:
        mylogger.error(_sql_str+str(e))
        mylogger.debug("end")
        pass
    return



if __name__ == '__main__':
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/airet/ai2filter.log")
    mylogger.info("start running")
    cur = get_a_sql_cur_forever(mylogger)
    ServerID = wtclib.get_serverID()
    try:
        time.sleep(random.random())
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet, ServerID)values(%d, "
                    "'python %s &', 300, %d,'%s')" % (os.getpid(), __file__, time.time(), ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "ai2filter" in _dic1:
            _version = _dic1["ai2filter"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai2filter','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
        os._exit()

    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"

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
        interval_sec = int(conf_dict["interval_sec"])
        if interval_sec < 10 or interval_sec > 300:
            _interval_sec = 60
    else:
        interval_sec = 60

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
                # channel.exchange_declare(exchange="AiOut",exchange_type="fanout", passive=False, durable=False, auto_delete=True)
                channel.queue_declare(queue="aifilter")
                channel.queue_bind(queue="aifilter", exchange=_mq_exchange)
                break
            except Exception, e:
                mylogger.info(str(e))
                time.sleep(20)
        channelOut = conn_broker.channel()

        channelOut.exchange_declare(exchange="AiOut.filter", exchange_type="fanout",
                                    passive=False, durable=False, auto_delete=True)
        channel.basic_consume(msg_consumer, queue="aifilter", consumer_tag="filter")

        try:
            channel.start_consuming()
        except Exception, e:
            mylogger.error(str(e))
            try:
                channel.close()
            except Exception, e:
                mylogger.error(str(e))
            try:
                channelOut.close()
            except Exception, e:
                mylogger.error(str(e))
