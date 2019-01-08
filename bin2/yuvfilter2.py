import random
import json
import os
import sys
import time

import pika

import wtclib


def get_rabbitmq_channel():
    global mylogger
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
    return channel


def get_a_sql_cur_forever(mylog):
    while True:
        (_cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
        if None != _cur:
            break
        else:
            mylog.info(err)
            time.sleep(20)
    return _cur

if __name__ == '__main__':
    if not os.path.isdir("../log/airet"):
        try:
            os.mkdir("../log/airet")
        except Exception, e:
            print str(e) + " in line: " + str(sys._getframe().f_lineno)
            os._exit()
    mylogger = wtclib.create_logging("../log/airet/yuvfilter.log")
    mylogger.info("start running")
    cur = get_a_sql_cur_forever(mylogger)




    conf_dict = wtclib.get_user_config_ret_dict("../conf/conf.conf", "plate")
    if "havecar_delay" in conf_dict:
        _haveCar_delay = int(conf_dict["havecar_delay"])
        if _haveCar_delay < 5 or _haveCar_delay > 600:
            _haveCar_delay = 30
    else:
        _haveCar_delay = 30

    channel = get_rabbitmq_channel()

    # msg = sys.argv[1]
    msg = "hello" + str(time.localtime())
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    #Sqlite_cur, sqlite_conn = wtclib.get_a_sqlite3_cur_forever(mylogger, "/tmp/softdog.db")
    _pid = os.getpid()
    try:
        ServerID = wtclib.get_serverID()
        #time.sleep(random.random())
        cur.execute("insert into WatchdogTable(pid, runCMD,watchSeconds,renewTimet,ServerID)values(%d, "
                    "'python %s &', 30, %d,'%s')" % (_pid, __file__, int(time.time()),ServerID))
    except Exception, e:
        mylogger.error(str(e) + time.asctime())
    _yuvfilter_rabbitmq_timet = int(time.time())
    while True:
        _timeSec = time.time()
        try:
            _sql_str = "select cameraID from SpaceYUVFilterBuffTable where YUVRenewTime<%d and YUVRenewTime<>0"%(int(_timeSec)-_haveCar_delay)
            a1 = cur.execute(_sql_str)
            mylogger.info("fetchmany(%d) need yuv files " % a1 + _sql_str)
            _msgs = set(cur.fetchall())
        except Exception, e:
            mylogger.error(_sql_str+str(e))
            if 'MySQL server has gone away' in str(e):
                cur = get_a_sql_cur_forever(mylogger)
            continue

        if _timeSec - _yuvfilter_rabbitmq_timet > 10:
            _yuvfilter_rabbitmq_timet = _timeSec
            try:
                cur.execute("update WatchdogTable set renewTimet=%d where pid=%d and ServerID='%s'" % (_timeSec, _pid,ServerID))
                msg = json.dumps({"msg":"alive%d"%_timeSec})
                mylogger.debug(msg)
                channel.basic_publish(body=msg, exchange="AiOut.yuvfilter", properties=msg_props, routing_key="hola")
            except Exception, e:
                mylogger.info(str(e))
                if 'MySQL server has gone away' in str(e):
                    cur = get_a_sql_cur_forever(mylogger)
                else:
                    try:
                        channel.close()
                    except Exception, e:
                        mylogger.error(str(e))
                    channel = get_rabbitmq_channel()

        if 0 == a1:
            time.sleep(0.5)
            continue

        for _sql in _msgs:

            msg = json.dumps({"sn": _sql[0], "from":"yuvfilter"})
            mylogger.info("rabbitmq publish:"+msg)

            try:
                channel.basic_publish(body=msg, exchange="AiOut.yuvfilter", properties=msg_props, routing_key="hola")
            except Exception, e:
                mylogger.info(str(e))
                try:
                    channel.close()
                except Exception, e:
                    mylogger.error(str(e))

                channel = get_rabbitmq_channel()

            try:
                cur.execute("update SpaceYUVFilterBuffTable set YUVRenewTime=0 where cameraID='%s'" % _sql[0])
            except Exception, e:
                mylogger.error(str(e))
                pass

        time.sleep(0.5)

