import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="place",exchange_type="direct", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue="place_queue")
channel.queue_bind(queue="place_queue", exchange="place", routing_key="place queue")

def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()
    else:
        print body
    return

channel.basic_consume(msg_consumer, queue="place_queue", consumer_tag="hello-consumer2")
channel.start_consuming()