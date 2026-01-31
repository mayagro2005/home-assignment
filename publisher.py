import pika
import time

# Wait for RabbitMQ
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                'rabbitmq',
                heartbeat=600  # <-- Added heartbeat to prevent timeout during interactive mode
            )
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying...")
        time.sleep(2)

channel = connection.channel()

# 1. Durable queue
channel.queue_declare(queue='ABC', durable=True)

# Send the required 10 messages
print("Sending 10 required messages...")
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

# BONUS: Keep publisher running for interactive messages
print("\n--- Bonus: Interactive Mode ---")
print("Type additional messages to send (Ctrl+C to exit):")

try:
    while True:
        message = input("> ")
        if message.strip():  # Only send non-empty messages
            channel.basic_publish(
                exchange='',
                routing_key='ABC',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
            print("Sent:", message)
except KeyboardInterrupt:
    print("\nClosing publisher...")
    connection.close()
