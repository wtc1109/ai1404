import pika, sys
import time,os
import json
import wtclib
import shutil

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
                             passive=False, durable=False, auto_delete=False)
    return channel



if __name__ == '__main__':
    Remq = get_plate_rabbitmq_channel()
    msg_props = pika.BasicProperties()
    msg_props.content_type = "text/plain"
    s = os.getcwd()
    root_dir = s[:s[0:s.rfind('/')].rfind('/')]
    del s
    cnt = 0
    while True:

        for snpath, hvpd_sns, filenames in os.walk('../../20180731'):
            print snpath

            break
        for _hvpd in hvpd_sns:
            filenames = os.listdir(snpath+"/%s"%_hvpd)

            for fyuv in filenames:
                if fyuv.find(".yuv") < 0:
                    continue
                fileinfo = fyuv.split('_')
                _w_h = fileinfo[-1].split('.')[0].split('x')
                _tmp_filename = "/tmp/ff_fe_%dx%d_%d.yuv"%(int(_w_h[0]),int(_w_h[1]),cnt&0x0F)
                shutil.copy(snpath+"/%s/"%_hvpd+fyuv, _tmp_filename)
                cnt += 1


                _LTx = 0
                _LTy = 0
                _RBx = int(_w_h[0])-1
                _RBy = int(_w_h[1])-1
                info = {"cam_id": _hvpd[:-1], "pic_full_name": _tmp_filename,
                        "Pic_type_for": "plate", "CMOS": 0,
                        "LTx": _LTx, "LTy": _LTy,
                        "RBx": _RBx, "RBy": _RBy,
                        "plateGet": int(fileinfo[0]), "AIfile": "1526969345_125.jpg","time_now":int(time.time())}
                js_msg = json.dumps(info)
                print len(js_msg)
                try:
                    print js_msg
                    print fyuv
                    Remq.basic_publish(body=js_msg, exchange="plate", properties=msg_props,
                                       routing_key="plate queue")
                except Exception, e:
                    mylogger.debug(str(e))
                    Remq = get_plate_rabbitmq_channel()
                time.sleep(0.5)
        time.sleep(10)