import ConfigParser
import json
import os
import sys
import time

import pika

import bin.wtclib

if __name__ == '__main__':
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = bin.wtclib.create_logging("../log/airet/yuvfilter.log")
    mylogger.info("start running")
    while True:
        (cur, err) = bin.wtclib.get_a_sql_cur("../conf/conf.conf")
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
            conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            break
    channel = conn_broker.channel()

    channel.exchange_declare(exchange="AiOut.yuvfilter", exchange_type="fanout",
                             passive=False, durable=False, auto_delete=True)

    # msg = sys.argv[1]
    msg = "hello" + str(time.localtime())
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"

    _pid = os.getpid()
    try:
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet)values(%d, "
                    "'python %s &', 30, %d)" % (_pid, __file__, int(time.time())))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
    _yuvfilter_rabbitmq_timet = int(time.time())
    while True:
        _timeSec = time.time()
        try:
            cur.execute("update WatchdogTable set renewTimet=%d where pid=%d" % (_timeSec, _pid))
            _sql_str = "select * from YUVFilterBuffTable where RenewTime<%d and RenewTime<>0"%(int(_timeSec)-5)#*60
            a1 = cur.execute(_sql_str)
        except Exception, e:
            mylogger.error(str(e))
            continue
        if 0 == a1:
            if _timeSec - _yuvfilter_rabbitmq_timet > 10:
                _yuvfilter_rabbitmq_timet = _timeSec
                try:
                    msg = json.dumps({"msg":"alive%d"%_timeSec})
                    mylogger.debug(msg)
                    channel.basic_publish(body=msg, exchange="AiOut.yuvfilter", properties=msg_props, routing_key="hola")
                except Exception, e:
                    mylogger.info(str(e))
                    try:
                        channel.close()
                    except Exception, e:
                        mylogger.error(str(e))
                    try:
                        conn_broker = pika.BlockingConnection(conn_params)
                        channel = conn_broker.channel()
                    except Exception, e:
                        mylogger.error(str(e))
                        os._exit()
            time.sleep(0.5)
            continue
        try:
            mylogger.debug("fetchmany: "+_sql_str)
            _msgs = cur.fetchmany(a1)
        except Exception, e:
            time.sleep(1)
            mylogger.info(str(e))
            continue
        for _sql in _msgs:
            try:
                _ai_out = cur.fetchmany(cur.execute("select * from AiOutTable where cameraID='%s' and cmosID=%d"%(_sql[2], _sql[3])))[0]
            except Exception, e:
                mylogger.info(str(e))
                continue
            if 1 == _ai_out[5+_sql[4]]:
                msg = json.dumps({"sn": _sql[2], "CMOS": _sql[3], "from":"yuvfilter", "place":_sql[4], "space":_sql[1]})
                mylogger.debug(msg)
                try:
                    channel.basic_publish(body=msg, exchange="AiOut.yuvfilter", properties=msg_props, routing_key="hola")
                except Exception, e:
                    mylogger.info(str(e))
                    try:
                        channel.close()
                    except Exception, e:
                        mylogger.error(str(e))
                    try:
                        conn_broker = pika.BlockingConnection(conn_params)
                        channel = conn_broker.channel()
                    except Exception, e:
                        mylogger.error(str(e))
                        os._exit()

                #_sql_str = "update SpaceStatusTable set CarportStatus=0 where Spaceid='%s'"%_sql[1]
                #mylogger.debug(_sql_str)
                #cur.execute(_sql_str)
            try:
                cur.execute("update YUVFilterBuffTable set RenewTime=0 where id=%d"%_sql[0])
            except Exception, e:
                mylogger.debug(str(e))
                pass
        time.sleep(0.5)