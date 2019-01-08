import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="place",exchange_type="direct", passive=False, durable=False, auto_delete=True)
channel.queue_declare(queue="aiqueue")
channel.queue_bind(queue="aiqueue", exchange="place", routing_key="place queue")

def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="aiconsumer")
        channel.stop_consuming()
    else:
        print body
    return

channel.basic_consume(msg_consumer, queue="aiqueue", consumer_tag="hello-consumer")
channel.start_consuming()