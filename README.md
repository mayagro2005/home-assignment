# Home Assignment: RabbitMQ + CPU Monitor

## Prerequisites

- Docker and Docker Compose installed
- Python 3.x installed
- pip installed

## Step 1 – Start RabbitMQ with Docker Compose

In the project folder, run:

```bash
docker-compose up -d

## Step 2 – Install Python dependencies

Install:
pip install pika psutil


## Step 3 – Start the consumer and the publisher
### Run
Open a terminal and run:

python consumer.py
It will wait for messages from queue ABC.


Open another terminal and run:

python publisher.py

You should see messages being sent in the publisher terminal and received in the consumer terminal.
---

## Step 5 – CPU Monitoring Service

Run:
python cpu_monitor.py

This will monitor CPU usage and print an alert if it goes above 80%.

---

## Step 6 – Stop RabbitMQ

docker-compose down

This stops and removes the RabbitMQ container.

## Bonus – Multicast

Multicast is one-to-many network communication used in video streaming, telemetry, and stock feeds.
To move multicast between networks, routers use IGMP and PIM or a multicast gateway.
