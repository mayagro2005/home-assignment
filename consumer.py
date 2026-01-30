import pika
import time

def callback(ch, method, properties, body):
    print("Received:", body.decode())

# Wait for RabbitMQ
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq')
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying...")
        time.sleep(2)

channel = connection.channel()

# Must match publisher exactly
channel.queue_declare(queue='ABC', durable=True)

channel.basic_consume(
    queue='ABC',
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for messages...")
channel.start_consuming()
