# Message Queue System with RabbitMQ

## Assignment: Publisher and Consumer Implementation

This project implements a simple message queuing system using **RabbitMQ** as the message broker.

### What it does:
- **Publisher**: Sends 10 messages to the "ABC" channel
- **Consumer**: Subscribes to the "ABC" channel and prints received messages

---

## Setup and Running

### Prerequisites
- Docker and Docker Compose installed

### Step 1: Start the system

docker-compose up --build

This will:
1. Start RabbitMQ container
2. Start the Consumer (waits for messages)
3. Start the Publisher (sends 10 messages)
4. Start the CPU Monitor (monitors system CPU, memory, and disk)

### Step 2: View the results

See consumer receiving messages:

docker logs consumer

See publisher sending messages:

docker logs publisher

### Step 3: Stop the system

docker-compose down

---

## Key Features

- Simple RabbitMQ publisher/consumer workflow
- CPU, Memory, Disk monitoring with alerts
- Tracks top CPU-consuming processes
- Real-time logging to console and file

---

## Bonus Feature: Interactive Publisher & Live Communication

After sending the required 10 messages, the publisher stays alive and accepts user input for additional messages. You can see real-time communication between publisher and consumer.

### Prerequisites for Interactive Mode
The publisher container must have `stdin_open: true` and `tty: true` in docker-compose.yml to support interactive input.

### How to use Live Communication:

Step 1 - Terminal 1: Start all containers

docker-compose down
docker-compose up --build

You should see output showing:
- RabbitMQ starting
- Consumer waiting for messages
- Publisher sending 10 messages
- Publisher entering interactive mode

Step 2 - Terminal 2: Attach to publisher to send messages

docker attach publisher

You can now type messages:
> Hello from terminal!
Sent: Hello from terminal!
> This is a test
Sent: This is a test

Step 3 - Terminal 3: View consumer messages in real-time

docker logs -f consumer

You'll see all messages appear in the consumer as they're sent:
Waiting for messages...
Received: Message number 0
Received: Message number 1
...
Received: Message number 9
Received: Hello from terminal!
Received: This is a test

To exit:
- Press Ctrl+C in Terminal 2 (publisher) to stop sending messages
- Press Ctrl+C in Terminal 3 (consumer logs) to stop watching logs
- Press Ctrl+C in Terminal 1 to stop all containers

Troubleshooting:
- If you get "cannot attach to a stopped container", run docker-compose up --build first
- Make sure you have stdin_open: true and tty: true in the publisher section of docker-compose.yml

---

## System Monitoring Service - Detailed Explanation

### Overview
The system_monitor.py service continuously monitors system-wide CPU, memory, and disk usage. It logs warnings when CPU usage exceeds 80%.

### Code Structure Explained

CONFIGURATION Section

THRESHOLD = 80              # Alert if CPU > 80%
CHECK_INTERVAL = 5          # Check every 5 seconds
ALERT_COOLDOWN = 300        # Wait 5 min before next alert

LOGGING Section

Logs appear in console (real-time) and are saved to system_monitor.log

GET TOP PROCESSES Function

Gets the 3 apps using the most CPU.

MAIN LOOP

- Grabs CPU, memory, disk every CHECK_INTERVAL seconds
- Logs the metrics
- If CPU > THRESHOLD and cooldown passed:
  - Logs a warning
  - Shows top CPU-consuming processes
- Repeats indefinitely

---

### Features

Real-time Monitoring
- Checks CPU, Memory, and Disk every 5 seconds
- Identifies top 3 processes consuming CPU
- Tracks all system metrics in one place

Advanced Logging
- Structured logs with timestamps
- File logging (system_monitor.log) + console output
- Different severity levels (INFO, WARNING, ERROR)

Smart Alerts
- Alert cooldown (5 minutes) to prevent alert spam
- Alert counter to track alert history
- Shows which processes are hogging CPU

---

### Running the System Monitor

Option 1: Via Docker Compose (included)

docker-compose up

Option 2: Standalone (on your machine)

python system_monitor.py

---

### Example Log Output

Normal operation:
2024-01-31 10:15:01 - INFO - CPU:  45.2% | Memory:  32.1% | Disk:  60.5%
2024-01-31 10:15:06 - INFO - CPU:  52.3% | Memory:  33.5% | Disk:  60.5%

High CPU detected:
2024-01-31 10:15:11 - WARNING - ALERT #1 CPU 85.6%
2024-01-31 10:15:11 - WARNING - Top processes:
 - python (28.5%)
 - chrome (15.2%)
 - docker (8.1%)

After cooldown period:
2024-01-31 10:20:15 - WARNING - ALERT #2 CPU 82.1%
2024-01-31 10:20:15 - WARNING - Top processes:
 - docker (18.5%)
 - python (12.3%)
 - node (5.1%)

---

### Log File

Logs are saved to system_monitor.log with full details:

tail -f system_monitor.log  # Watch logs in real-time

---

## Project Structure

- publisher.py - Sends 10 messages to "ABC" queue + bonus interactive mode
- consumer.py - Listens to "ABC" queue and prints messages
- system_monitor.py - Monitors CPU/Memory/Disk usage with advanced logging
- docker-compose.yml - Orchestrates all services
- Dockerfile.publisher, Dockerfile.consumer, Dockerfile.cpu - Container configurations
- system_monitor.log - Generated log file from system monitor
