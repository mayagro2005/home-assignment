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

```bash
docker-compose up --build
```

This will:
1. Start RabbitMQ container
2. Start the Consumer (waits for messages)
3. Start the Publisher (sends 10 messages)
4. Start the CPU Monitor (monitors system CPU)

### Step 2: View the results

**See consumer receiving messages:**
```bash
docker logs consumer
```

**See publisher sending messages:**
```bash
docker logs publisher
```

### Step 3: Stop the system

```bash
docker-compose down
```

---

## Key Features

---

## Bonus Feature: Interactive Publisher & Live Communication

After sending the required 10 messages, the publisher stays alive and accepts user input for additional messages. You can see real-time communication between publisher and consumer!

### Prerequisites for Interactive Mode
The publisher container must have `stdin_open: true` and `tty: true` in docker-compose.yml to support interactive input.

### How to use Live Communication:

**Step 1 - Terminal 1: Start all containers**
```bash
docker-compose down   # Stop any previous containers
docker-compose up --build
```

You should see output showing:
- RabbitMQ starting
- Consumer waiting for messages
- Publisher sending 10 messages
- Publisher entering interactive mode

**Step 2 - Terminal 2: Attach to publisher to send messages**
```bash
docker attach publisher
```

**IMPORTANT:** Only run this after you see the `> ` prompt in Terminal 1. The publisher must be running first.

You can now type messages:
```
> Hello from terminal!
Sent: Hello from terminal!
> This is a test
Sent: This is a test
```

**Step 3 - Terminal 3: View consumer messages in real-time**
```bash
docker logs -f consumer
```

You'll see all messages appear in the consumer as they're sent:
```
Waiting for messages...
Received: Message number 0
Received: Message number 1
...
Received: Message number 9
Received: Hello from terminal!
Received: This is a test
```

**To exit:**
- Press `Ctrl+C` in Terminal 2 (publisher) to stop sending messages and close the publisher
- Press `Ctrl+C` in Terminal 3 (consumer logs) to stop watching logs
- Press `Ctrl+C` in Terminal 1 to stop all containers

**Troubleshooting:**
- If you get "cannot attach to a stopped container", run `docker-compose up --build` first
- Make sure you have `stdin_open: true` and `tty: true` in the publisher section of docker-compose.yml

---

## Project Structure

- `publisher.py` - Sends 10 messages to "ABC" queue
- `consumer.py` - Listens to "ABC" queue and prints messages
- `docker-compose.yml` - Orchestrates all services
- `Dockerfile.publisher`, `Dockerfile.consumer` - Container configurations
