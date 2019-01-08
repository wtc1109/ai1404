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
mylogger = wtclib.create_logging("../log/airet/ai2led.log")
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

        mylogger.debug("msg recv "+body)
        if not "sn" in _dic_info:
            return
        if not "CMOS" in _dic_info:
            return
        _cmos = _dic_info["CMOS"]

        if 0 == cur.execute("select * from AiOutTable where cameraID='%s' and cmosID=%d"%(_dic_info["sn"], _cmos)):
            return
        _ai_out = cur.fetchmany(1)[0]
        if 0 == cur.execute("select * from AiOutFilterTable where cameraID='%s' and cmosID=%d"%(_dic_info["sn"], _cmos)):
            _timeSec = int(time.time())
            cur.execute("insert into AiOutFilterTable(cameraID, cmosID, parking1StateList, parking2StateList, "
                        "parking3StateList, parking1TimeList, parking2TimeList, parking3TimeList)values('%s', %d,'%d',"
                        "'%d', '%d', '%d', '%d', '%d')"%(_dic_info["sn"], _cmos, _ai_out[5], _ai_out[6], _ai_out[7],
                                                         _timeSec, _timeSec, _timeSec))
        _aiFilter_out = cur.fetchmany(1)[0]
        _parking1StateList = _aiFilter_out[2].split(',')
        _parking2StateList = _aiFilter_out[3].split(',')
        _parking3StateList = _aiFilter_out[4].split(',')
        _parking1TimeList = _aiFilter_out[5].split(',')
        _parking2TimeList = _aiFilter_out[6].split(',')
        _parking3TimeList = _aiFilter_out[7].split(',')
        _parkingState = []
        for i in range(3):
            _parkingState.append(_ai_out[5])
        if 1 != len(_parking1StateList):
            if '1' == _parking1StateList[len(_parking1StateList)-1]:
                _parkingState[0] = 1
            else:
                if '0' == _parking1StateList[len(_parking1StateList) - 2]:
                    _parkingState[0] = 0

            if '1' == _parking2StateList[len(_parking2StateList)-1]:
                _parkingState[1] = 1
            if '1' == _parking3StateList[len(_parking3StateList)-1]:
                _parkingState[2] = 1

        _hvpd = _dic_info["sn"]
        if 1 == _cmos:
            _offset = 4
        else:
            _offset = 1
        for i in range(3):

            if 0 == cur.execute("select * from SpaceStatusTable where Spaceid='%s%d'"%(_hvpd, (i+_offset))):
                continue
            (_space_for, ) = cur.fetchmany(cur.execute("select CarportStatus from SpaceStatusTable where Spaceid='%s%d'"%(_hvpd, (i+_offset))))[0]
            if 0 == _space_for or 1 == _space_for:  #others for reserved
                cur.execute("update SpaceStatusTable set CarportStatus = %d where Spaceid='%s%d'"%(_parkingState[i], _hvpd, (i+_offset)))


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
    channel.queue_declare(queue="leddisplayer")
    channel.queue_bind(queue="leddisplayer", exchange=_mq_exchange)



    channel.basic_consume(msg_consumer, queue="leddisplayer", consumer_tag="led")
    channel.start_consuming()