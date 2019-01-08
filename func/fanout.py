import pika, sys
import time
import json

credentials = pika.PlainCredentials("wutao", "12345678")
#conn_params = pika.ConnectionParameters(host= "localhost",port=5672, credentials=credentials)
conn_params = pika.ConnectionParameters(host= "192.168.7.19",port=5672, virtual_host="OutTrig", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="AiOut.tr", exchange_type="fanout",
                         passive=False, durable=False, auto_delete=True)


channel2 = conn_broker.channel()

channel2.exchange_declare(exchange="ReOut.tr", exchange_type="fanout",
                         passive=False, durable=False, auto_delete=True)
#msg = sys.argv[1]
msg = "hello" + str(time.localtime())
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

#channel.basic_publish(body=msg, exchange="AiOut.tr", properties=msg_props,routing_key="hola")

while True:


    msg = json.dumps({"cam_id":"1804430019","CMOS":0})
    channel.basic_publish(body=msg, exchange="AiOut.tr", properties=msg_props,
                          routing_key="hola")
    channel2.basic_publish(body=msg, exchange="ReOut.tr", properties=msg_props,
                          routing_key="hola")
    print "producer running" + msg
    time.sleep(5)
    msg = json.dumps({"cam_id": "1804430021", "CMOS": 0})
    channel.basic_publish(body=msg, exchange="AiOut.tr", properties=msg_props,
                          routing_key="hola")
    channel2.basic_publish(body=msg, exchange="ReOut.tr", properties=msg_props,
                           routing_key="hola")
    print "producer running" + msg
    time.sleep(5)
    msg = json.dumps({"cam_id":"1805430035", "CMOS": 0})
    channel.basic_publish(body=msg, exchange="AiOut.tr", properties=msg_props,
                          routing_key="hola")
    channel2.basic_publish(body=msg, exchange="ReOut.tr", properties=msg_props,
                          routing_key="hola")

    print "producer running" + msg
    time.sleep(5)