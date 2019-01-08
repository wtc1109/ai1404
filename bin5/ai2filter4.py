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

def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf","hvpd3db2")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur



def wdi(cur):
    global mylogger,ServerID
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (int(time.time()), os.getpid(),ServerID))
    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)


def msg_consumer(channel, method, header, body):
    global cur, mylogger, channelOut, msg_props, interval_sec

    channel.basic_ack(delivery_tag=method.delivery_tag)
    _timeSec = int(time.time())
    wdi(cur)
    mylogger.info("msg recv" + body)
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
            cur.execute("update aisoftwareversion set warning=%s where SoftwareName='ai'"%_dic_info["aimsg"])
        except Exception,e:
            mylogger.error(str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylogger)
        finally:
            return
    if not "cam_id" in _dic_info:
        mylogger.info("not cam_id in %s"%body)
        try:
            mylogger.debug("basic_publish:" + body + " @ %d" % _timeSec)
            channelOut.basic_publish(body=body, exchange="AiOut.filter", properties=msg_props, routing_key="hola")
        except Exception, e:
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()
            mylogger.error("channelOut Error " + str(e))
        return
    if not "CMOS" in _dic_info:
        mylogger.info("not CMOS in _dic_info")
        return
    if not type(_dic_info["CMOS"])==int:
        mylogger.info("not type CMOS is int")
        return



    try:
        _sql_str = "select cameraID,cmosID,bay,State from aiouttable_bay where cameraID='%s' and cmosID=%d" \
                   % (_dic_info["cam_id"], _dic_info["CMOS"])
        if 0 == cur.execute(_sql_str):
            mylogger.debug("None= "+_sql_str)
            return
        _ai_outs = sorted(cur.fetchall())

        _sql_str = "select bays from aisettingtable_camera_mem where cameraID='%s' and cmosID=%d"\
                   %(_dic_info["cam_id"], _dic_info["CMOS"])
        cur.execute(_sql_str)
        (_bays,) = cur.fetchone()

    except Exception, e:
        mylogger.error(str(e))
        if 'MySQL server has gone away' in str(e):
            cur = get_a_sql_cur_forever(mylogger)

    try:
        _need_rabbitmq = 0
        _sql_str = "select bay,CarportStatus,YUVGetfilesTime,Lamp_changeTime from SpaceStatusTable where cameraID='%s' and cmosID=%d " \
                   % (_dic_info["cam_id"], _dic_info["CMOS"])
        if 0 == cur.execute(_sql_str):
            return
        _status_infos = sorted(cur.fetchall())
        if None == _status_infos:
            return
        _bay_change = []
        for i in range(_bays):
            _ai_out = _ai_outs[i]
            _status_info = _status_infos[i]
            if _ai_out[2] != _status_info[0]:
                continue

            if 1 != _ai_out[3] and 0 != _ai_out[3]:
                continue
            _sql_str2 = ""
            _sql_str = ''
            _sql_str3 = ''
            if _status_info[1] != _ai_out[3]:#change
                _need_rabbitmq = 1
                _bay_change.append(i)
                _sql_str2 = "update SpaceStatusTable set Status_changeTime=%d, CarportStatus=%d where cameraID='%s' " \
                            "and cmosID=%d and bay=%d" % (_timeSec, _ai_out[3], _ai_out[0], _ai_out[1], _ai_out[2])
                if 0 == _ai_out[3]:#car is leaving,delay to change lamp
                    _sql_str = "update SpaceStatusTable set StatusChange0Time=%d, parkout_timet=%d,parkout_time=now()" \
                               " where cameraID='%s' and cmosID=%d and bay=%d and StatusChange0Time=0" \
                               % (_timeSec,_timeSec, _ai_out[0], _ai_out[1], _ai_out[2])
                else:#car is coming, change lamp immediately
                    #mylogger.info("bay%d aiout is %d, cur is %d"%(i+1, _ai_out[3], _status_info[1]))

                    _sql_str = "update SpaceStatusTable set YUVRenewTime=%d" \
                               " where cameraID='%s' and cmosID=%d and bay=%d and YUVRenewTime=0" \
                               % (_timeSec,_ai_out[0], _ai_out[1], _ai_out[2])
                    _sql_str3 = "update SpaceStatusTable set parkin_timet=%d,parkin_time=now() " \
                                "where cameraID='%s' and cmosID=%d and bay=%d"\
                                %(_timeSec,_ai_out[0], _ai_out[1], _ai_out[2])

            else:#no change
                if 1 == _ai_out[3] and _timeSec - _status_info[2] > 4*60:
                    _sql_str = "update SpaceStatusTable set YUVRenewTime=%d " \
                               " where cameraID='%s' and cmosID=%d and bay=%d and YUVRenewTime=0" \
                               % (_timeSec,_ai_out[0], _ai_out[1], _ai_out[2])

            try:
                if _sql_str != '':
                    cur.execute(_sql_str)
                if _sql_str2 != '':
                    cur.execute(_sql_str2)
                if _sql_str3 != '':
                    cur.execute(_sql_str3)
            except Exception,e:
                mylogger.error(_sql_str+str(e))

            if _timeSec - _status_info[3] > 5 * 60:
                #mylogger.info("Lamp_changeTime is %d ,now is %d"%(_status_info[3], _timeSec))
                _need_rabbitmq = 2


        if 0 != _need_rabbitmq:
            if len(_bay_change) > 0:
                _sql_str = "select startAIout from video_rtsp2mp4_table where cameraID='%s' and ServerID != null" % _dic_info[
                    "cam_id"]
                if 0 != cur.execute(_sql_str):
                    _video_table, = cur.fetchone()
                    if None != _video_table:
                        _startAIout = ''
                        for i in range(_ai_out[4]):
                            if i in _bay_change:
                                _startAIout += '4'
                            else:
                                _startAIout += _video_table[1][i]

                        _sql_str = "update video_rtsp2mp4_table set startAIout='%s' where cameraID='%s'" \
                                   "" % (_startAIout, _dic_info["cam_id"])
                        cur.execute(_sql_str)

            msg = json.dumps({"sn": _ai_out[0], "CMOS": _ai_out[1]})
            try:
                mylogger.info("basic_publish:"+msg+" @ %d"%_timeSec)
                channelOut.basic_publish(body=msg, exchange="AiOut.filter", properties=msg_props,routing_key="hola")
            except Exception, e:
                if True == channelOut.is_closed:
                    channel.basic_cancel(consumer_tag="hello-consumer2")
                    channel.stop_consuming()
                    mylogger.error("channelOut Error "+str(e))

    except Exception,e:
        mylogger.error(str(e))
        mylogger.error(_sql_str)
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
    #sqlite3_cur, sqlite3_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    try:
        ServerID = wtclib.get_serverID()
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 300, %d,'%s')" % (os.getpid(), __file__, time.time(),ServerID))
        _dic1 = wtclib.get_user_config_ret_dict("aisoftversion.ini", "version")
        if "ai2filter" in _dic1:
            _version = _dic1["ai2filter"]
        else:
            stat = os.stat(__file__)
            _version = datetime.date.fromtimestamp(stat.st_mtime).isoformat()
        cur.execute("insert into AiSoftwareVersion(SoftwareName, version)values('ai2filter','%s')"
                    "ON DUPLICATE KEY UPDATE version='%s'" % (_version, _version))
        del _dic1
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
    del conf_dict

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
