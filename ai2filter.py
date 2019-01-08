import MySQLdb
import pika
import time
import json
import urllib
import urllib2
import os, sys
import requests
from bin import wtclib
import ConfigParser

if not os.path.isdir("../log/airet"):
    try:
        os.mkdir("../log/airet")
    except Exception, e:
        print str(e) + " in line: " + str(sys._getframe().f_lineno)
        os._exit()
mylogger = wtclib.create_logging("../log/airet/ai2filter.log")
mylogger.info("start running")
while True:
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
    if None != cur:
        break
    else:
        mylogger.info("can not connect to db and sleep 20")
        time.sleep(20)

_cf = ConfigParser.ConfigParser()
try:
    _cf.read("../conf/conf.conf")
except Exception, e:
    mylogger.error(str(e))
    os._exit(0)
_secs = _cf.sections()
try:
    _opts = _cf.options("rabbitmq")
except Exception, e:
    mylogger.error(str(e)+' rabbitmq')
    os._exit(0)
try:
    _mq_host = _cf.get("rabbitmq", "AiOutmq_server_addr")
    _mq_port = _cf.getint("rabbitmq", "AiOutmq_server_port")
    _mq_exchange = _cf.get("rabbitmq", "AiOutmq_exchange")
    _mq_user_name = _cf.get("rabbitmq", "AiOutmq_user_name")
    _mq_passwd = _cf.get("rabbitmq", "AiOutmq_passwd")
    _mq_vhost = _cf.get("rabbitmq", "AiOutmq_vhost")
except Exception, e:
    mylogger.error(str(e)+' get AiOutmq')
    os._exit(0)
del _cf
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
        channel.queue_declare(queue="aifilter")
        channel.queue_bind(queue="aifilter", exchange=_mq_exchange)
        break
    except Exception, e:
        mylogger.info(str(e))
        time.sleep(20)
channelOut = conn_broker.channel()

channelOut.exchange_declare(exchange="AiOut.filter", exchange_type="fanout",
                         passive=False, durable=False, auto_delete=True)
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"


def msg_consumer(channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        global cur, mylogger, channelOut, msg_props
        mylogger.debug("msg recv" + body)
        try:
            _dic_info = json.loads(body)
        except Exception, e:
            mylogger.warning(str(e))
            mylogger.warning("len = %d"%len(body))
            mylogger.warning("json.loads "+body)
            return
        if "quit" in _dic_info:
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()
            mylogger.debug("quit")
        mylogger.debug(body)
        if not "cam_id" in _dic_info:
            mylogger.debug("not cam_id in _dic_info")
            return
        if not "CMOS" in _dic_info:
            mylogger.debug("not CMOS in _dic_info")
            return
        elif not type(_dic_info["CMOS"])==int:
            mylogger.debug("not type CMOS is int")
            return
        _cmos = _dic_info["CMOS"]

        _sql_str = "select * from AiOutTable where cameraID='%s' and cmosID=%d"%(_dic_info["cam_id"], _cmos)
        if 0 == cur.execute(_sql_str):
            mylogger.debug(_sql_str)
            return
        try:
            _ai_out = cur.fetchmany(1)[0]
        except:
            mylogger.debug("read select * from AiOutTable = 0")
            return
        _hvpd = _dic_info["cam_id"]
        if 1 == _cmos:
            _offset = 4
        else:
            _offset = 1
        _timeSec = int(time.time())
        try:
            for i in range(3):
                try:
                    (_space_for, ) = cur.fetchmany(cur.execute("select CarportStatus from SpaceStatusTable where Spaceid='%s%d'"%(_hvpd, (i+_offset))))[0]
                except:
                    mylogger.debug("read select CarportStatus from SpaceStatusTable")
                    continue
                if 1 == _space_for and 0 == _ai_out[5 + i]: #delay for lamp change
                    """when car is leaving, delay for check the car is leave, and get yuv is no necessary, so delete the buffer"""
                    cur.execute("insert into SpaceFilterBuffTable(Spaceid, cameraID, cmosID, CarPos, RenewTime)values"
                                "('%s', '%s', %d, %d, %d)"%(_hvpd+str(i+_offset), _hvpd, _cmos,i, _timeSec))
                    try:
                        cur.execute("delete from YUVFilterBuffTable where Spaceid='%s%d'" % (_hvpd, (i + _offset)))
                    except:
                        mylogger.debug("delete from YUVFilterBuffTable")
                        pass
                else:
                    """when car is comming, not check car leaving. and maybe a yuv file is necessary"""
                    cur.execute("update SpaceStatusTable set CarportStatus=%d, RenewTime=%d where Spaceid='%s%d'"
                                %(_ai_out[5 + i], _timeSec, _hvpd, (i + _offset)))
                    if 1 == _ai_out[5+i]:
                        try:
                            cur.execute("delete from SpaceFilterBuffTable where Spaceid='%s%d'"%(_hvpd, (i + _offset)))
                        except:
                            mylogger.debug("delete from SpaceFilterBuffTable")
                            pass

                        try:
                            (_RenewTime,) = cur.fetchmany(cur.execute(
                                "select RenewTime from YUVRenewTimeTable where Spaceid='%s%d'" % (
                                _hvpd, (i + _offset))))[0]
                        except Exception, e:
                            mylogger.debug("select RenewTime from YUVRenewTimeTable "+str(e))
                            _RenewTime = 0
                        if 0 == _space_for or ((_timeSec - _RenewTime)>5*60):
                            cur.execute(
                                "insert into YUVFilterBuffTable(Spaceid, cameraID, cmosID, CarPos, RenewTime)values"
                                "('%s', '%s', %d, %d, %d)" % (_hvpd + str(i + _offset), _hvpd, _cmos, i, _timeSec))
                            cur.execute("insert into YUVRenewTimeTable(Spaceid, RenewTime)values('%s', %d)"
                                        "ON DUPLICATE KEY update RenewTime=%d"%(_hvpd + str(i + _offset),_timeSec, _timeSec))

            msg = json.dumps({"sn": _hvpd, "CMOS": _cmos})
            try:
                mylogger.debug("basic_publish:"+msg)
                channelOut.basic_publish(body=msg, exchange="AiOut.filter", properties=msg_props,routing_key="hola")
            except:
                mylogger.warning("channelOut.basic_publish")

        except:
            mylogger.debug("end")
            pass
        return


if __name__ == '__main__':
    channel.basic_consume(msg_consumer, queue="aifilter", consumer_tag="filter")
    channel.start_consuming()