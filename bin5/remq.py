import pika, sys
import time,os
import json
import wtclib

def get_plate_rabbitmq_channel():
    global mylogger
    while True:
        try:
            credentials = pika.PlainCredentials("guest", "guest")
            conn_params = pika.ConnectionParameters(host="localhost", virtual_host="/", credentials=credentials,
                                                    heartbeat=60, connection_attempts=5)
            conn_broker = pika.BlockingConnection(conn_params)
            break
        except Exception, e:
            mylogger.info(str(e))
            time.sleep(20)

    channel = conn_broker.channel()
    channel.exchange_declare(exchange="plate", exchange_type="direct",
                             passive=False, durable=True, auto_delete=False)
    return channel



if __name__ == '__main__':
    Remq = get_plate_rabbitmq_channel()
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    s = os.getcwd()
    root_dir = s[:s[0:s.rfind('/')].rfind('/')]
    del s
    while True:
        for snpath, dayname, filenames in os.walk('../../re/save_orig_yuv'):
            print snpath
            print dayname
            break
        for day1 in dayname:
            for snpath, hvpd_sns, filenames in os.walk('../../re/save_orig_yuv/%s'%day1):
                print snpath
                print dayname
                break
            for _hvpd in hvpd_sns:
                for snpath, hvpd_sns, filenames in os.walk(snpath+"/%s"%_hvpd):
                    print snpath
                    print dayname
                    break
                for fyuv in filenames:
                    if fyuv.find(".yuv") < 0:
                        continue
                    fileinfo = fyuv.split('_')
                    if '0' == fileinfo[-2] and '0' == fileinfo[-3] and\
                        '0' == fileinfo[-4] and '0' == fileinfo[-5]:
                        print "0000000000-00000-0000"
                        continue
                    _LTx = fileinfo[-5]
                    _LTy = fileinfo[-4]
                    _RBx = fileinfo[-3]
                    _RBy = fileinfo[-2]
                    info = {"cam_id": _hvpd[:-1], "pic_full_name": snpath+"/"+fyuv,
                            "Pic_type_for": "plate", "CMOS": 0,
                            "LTx": _LTx, "LTy": _LTy,
                            "RBx": _RBx, "RBy": _RBy,
                            "plateGet": 55, "AIfile": "1526969345_1804430019_0_0_368325.jpg"}
                    js_msg = json.dumps(info)
                    print len(js_msg)
                    try:
                        print js_msg
                        Remq.basic_publish(body=js_msg, exchange="plate", properties=msg_props,
                                           routing_key="plate queue")
                    except Exception, e:
                        mylogger.debug(str(e))
                        Remq = get_plate_rabbitmq_channel()
                    time.sleep(0.5)