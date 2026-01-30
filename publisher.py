import pika
import time

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

# 1. Durable queue
channel.queue_declare(queue='ABC', durable=True)

for i in range(10):
    message = f"Message number {i}"

    # 2. Persistent message
    channel.basic_publish(
        exchange='',
        routing_key='ABC',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # <-- THIS IS THE MAGIC
        )
    )

    print("Sent:", message)
    time.sleep(1)

connection.close()
