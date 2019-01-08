import ConfigParser
import json
import os
import time

import pika

from bin import wtclib

if not os.path.isdir("../log/airet"):
    try:
        os.mkdir("../log/airet")
    except Exception, e:
        print e
        os._exit()
mylogger = wtclib.create_logging("../log/airet/ai2getyuv.log")
mylogger.info("start running")
while True:
    (cur, err) = wtclib.get_a_sql_cur("../conf/conf.conf")
    if None != cur:
        break
    else:
        mylogger.info("can not connect to db and sleep 20")
        time.sleep(20)


def msg_consumer(channel, method, header, body):
        #channel.basic_ack(delivery_tag=method.delivery_tag)
        global cur, mylogger
        #test = cur.execute("select * from ScreenConfigTable")
        _dic_info = json.loads(body)
        if "quit" in _dic_info:
            channel.basic_cancel(consumer_tag="hello-consumer2")
            channel.stop_consuming()

        mylogger.debug("msg recv " + body)
        if not "sn" in _dic_info:
            return
        if "CMOS" in _dic_info:
            _cmos = _dic_info["CMOS"]
        a1 = cur.execute("select * from AiOutTable where cameraID=%s" % (_dic_info["sn"] + str(_cmos)))
        if 0 == a1:
            return
        _ai_out = cur.fetchmany(a1)[0]
        _hvpd = _dic_info["sn"]
        if '1' == _cmos:
            _offset = 4
        else:
            _offset = 1
        for i in range(_offset, _offset+3):
            b1 = cur.execute("select * from SpaceStatusTable where sn='%s%d'"%(_hvpd, i))
            if 0 == b1:
                continue
            _space_for = cur.fetchmany(cur.execute("select CarportStatus from SpaceStatusTable where Spaceid='%s%d'"%(_hvpd, i)))
            if 0 == _space_for or 1 == _space_for:  #others for reserved
                cur.execute("update SpaceStatusTable set CarportStatus = %d where Spaceid='%s%d'"%(_ai_out[10], _hvpd, i))


        return

if __name__ == '__main__':
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

    credentials = pika.PlainCredentials(_mq_user_name, _mq_passwd)
    conn_params = pika.ConnectionParameters(host=_mq_host, virtual_host=_mq_vhost, credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()

    #channel.exchange_declare(exchange="AiOut",exchange_type="fanout", passive=False, durable=False, auto_delete=True)
    channel.queue_declare(queue="hvpd_lamp")
    channel.queue_bind(queue="hvpd_lamp", exchange=_mq_exchange)



    channel.basic_consume(msg_consumer, queue="hvpd_lamp", consumer_tag="hvpd_lamp")
    channel.start_consuming()