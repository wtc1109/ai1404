import pika, sys
import time

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters(host= "localhost",port=5672, credentials=credentials)
#conn_params = pika.ConnectionParameters(host= "192.168.7.19",port=5672, credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel2 = conn_broker.channel()
channel.exchange_declare(exchange="hello-exchange", exchange_type="direct",
                         passive=False, durable=True, auto_delete=False)
channel2.exchange_declare(exchange="hello-exchange", exchange_type="direct",
                         passive=False, durable=True, auto_delete=False)
#msg = sys.argv[1]
msg = "hello" + str(time.localtime())
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props2 = pika.BasicProperties()
msg_props2.content_type = "text/plain"
channel.basic_publish(body=msg, exchange="hello-exchange", properties=msg_props,
                      routing_key="hola")
channel.basic_publish(body=msg, exchange="hello-exchange", properties=msg_props2,
                      routing_key="hola2")
while True:
    print "producer running" + msg
    time.sleep(10)
    msg = "hello" + str(time.localtime())
    channel.basic_publish(body=msg, exchange="hello-exchange", properties=msg_props,
                          routing_key="hola")
    channel2.basic_publish(body=msg, exchange="hello-exchange", properties=msg_props,
                          routing_key="hola2")