import ConfigParser
import json
import os
import sys
import time

import pika

import bin.wtclib


def create_wdt(cur):
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 30, %d)" % (os.getpid(), __file__, int(time.time())))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
        return -1
    return 0

def wdi(cur):
    global mylogger
    try:
        cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (int(time.time()), os.getpid()))
    except Exception, e:
        mylogger.error(str(e))

def rabbitmq_msg_alive(channel):
    global mylogger
    try:
        msg = json.dumps({"msg": "alive%d" % _timeSec})
        mylogger.debug(msg)
        channel.basic_publish(body=msg, exchange="AiOut.filter", properties=msg_props, routing_key="hola")
    except Exception, e:
        mylogger.error(str(e))
        return -1
    return 0

def get_user_configs():
    global mylogger
    _cf = ConfigParser.ConfigParser()
    try:
        _cf.read("../conf/conf.conf")
    except Exception, e:
        mylogger.error(str(e))
        os._exit(0)
    _secs = _cf.sections()

    try:
        _opts = _cf.options("aiplace")
    except Exception, e:
        mylogger.error(str(e) + ' aiplace')
        os._exit(0)

    try:
        _noCar_delay = _cf.getint("aiplace", "noCar_delay")
        if _noCar_delay < 2 or _noCar_delay > 20:
            _noCar_delay = 4
    except Exception, e:
        mylogger.error(str(e) + ' get aiplace')
        return -1, None
    del _cf
    return 0, _noCar_delay

def get_rabbitmq_channel():
    global mylogger
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
        mylogger.error(str(e) + ' rabbitmq')
        os._exit(0)
    try:
        _mq_host = _cf.get("rabbitmq", "AiOutmq_server_addr")
        _mq_port = _cf.getint("rabbitmq", "AiOutmq_server_port")
        _mq_exchange = _cf.get("rabbitmq", "AiOutmq_exchange")
        _mq_user_name = _cf.get("rabbitmq", "AiOutmq_user_name")
        _mq_passwd = _cf.get("rabbitmq", "AiOutmq_passwd")
        _mq_vhost = _cf.get("rabbitmq", "AiOutmq_vhost")
    except Exception, e:
        mylogger.error(str(e) + ' get AiOutmq')
        os._exit(0)

    del _cf
    while True:
        try:
            credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="AiOut.filter", exchange_type="fanout",
                             passive=False, durable=False, auto_delete=True)
    return channel


def get_mysql_cur():
    while True:
        (cur, err) = bin.wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != cur:
            break
        else:
            mylogger.info("can not connect to db and sleep 20")
            time.sleep(20)
    return cur


if __name__ == '__main__':
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = bin.wtclib.create_logging("../log/airet/aifilter.log")
    mylogger.info("start running")
    cur = get_mysql_cur()
    channel = get_rabbitmq_channel()
    (_ret, _noCar_delay) = get_user_configs()
    if 0 != _ret:
        _noCar_delay = 4

    #msg = "hello" + str(time.localtime())
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    _wdtRet = create_wdt(cur)
    _aifilter_rabbitmq_timet = int(time.time())
    _wdi_timet = _aifilter_rabbitmq_timet

    while True:
        _timeSec = time.time()
        if 0 == _wdtRet and _timeSec - _wdi_timet > 10:
            _wdi_timet = _timeSec
            wdi(cur)

        try:
            a1 = cur.execute("select * from SpaceFilterBuffTable where RenewTime<%d and RenewTime<>0"%(int(_timeSec-_noCar_delay)))
        except Exception, e:
            mylogger.error(str(e))
            cur = get_mysql_cur()
            continue
        if 0 == a1:
            if _timeSec - _aifilter_rabbitmq_timet > 10:
                _aifilter_rabbitmq_timet = _timeSec
                _ret = rabbitmq_msg_alive(channel)
                if 0 != _ret:
                    channel = get_rabbitmq_channel()
            time.sleep(0.5)
            continue

        try:
            _msgs = cur.fetchmany(a1)
        except Exception, e:
            mylogger.debug(str(e))
            time.sleep(1)
            continue
        for _sql in _msgs:
            try:
                _sql_str = "select * from AiOutTable where cameraID='%s' and cmosID=%d"%(_sql[2], _sql[3])
                _ai_out = cur.fetchmany(cur.execute(_sql_str))[0]
                mylogger.debug(_sql_str)
            except Exception, e:
                mylogger.error(str(e))
                mylogger.error(_sql_str)
                continue
            if 0 == _ai_out[5+_sql[4]]:
                msg = json.dumps({"sn": _sql[2], "CMOS": _sql[3], "from":"delay"})
                try:
                    _sql_str = "select * from SpaceStatusTable where Spaceid='%s'" % _sql[1]
                    _space_info = cur.fetchmany(cur.execute(_sql_str))[0]
                except Exception, e:
                    mylogger.error(str(e))
                    continue
                try:

                    if 0 != _space_info[3] or _timeSec > _space_info[4] + _noCar_delay:
                        channel.basic_publish(body=msg, exchange="AiOut.filter", properties=msg_props, routing_key="hola")
                    _sql_str = "update SpaceStatusTable set CarportStatus=0, RenewTime=%d where Spaceid='%s'"%(int(_timeSec),_sql[1])
                    mylogger.debug(_sql_str)
                    cur.execute(_sql_str)
                except Exception, e:
                    mylogger.error(str(e))
                    channel = get_rabbitmq_channel()

            try:
                cur.execute("update SpaceFilterBuffTable RenewTime=0 where Spaceid='%s'"%_sql[0])
            except Exception, e:
                mylogger.error(str(e))

        time.sleep(0.5)