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

## System Monitoring Service - Detailed Explanation

### Overview
The `system_monitor.py` service continuously monitors system-wide **CPU, memory, and disk** usage. It sends alerts when CPU usage exceeds 80%.

### Code Structure Explained

**1. CONFIGURATION Section (Lines 10-22)**
```python
THRESHOLD = 80              # Alert if CPU > 80%
CHECK_INTERVAL = 5          # Check every 5 seconds
ALERT_COOLDOWN = 300        # Wait 5 min before next alert
SEND_EMAIL_ALERTS = ...     # Enable/disable email
```
These are the **settings** you can customize.

**2. LOGGING Section (Lines 24-33)**
```python
logging.basicConfig(
    handlers=[
        logging.FileHandler('system_monitor.log'),  # Saves to file
        logging.StreamHandler()                     # Prints to console
    ]
)
```
This sets up **two-way logging**:
- ✅ Logs appear in console (real-time)
- ✅ Logs saved to `system_monitor.log` (permanent record)

**3. EMAIL ALERT Function (Lines 44-79)**
```python
def send_email_alert(cpu_usage, memory_usage, top_processes):
    # Checks if email is enabled
    if not SEND_EMAIL_ALERTS:
        return False
    
    # Composes email with metrics
    subject = f"HIGH CPU ALERT: {cpu_usage}%"
    body = f"CPU: {cpu_usage}%, Memory: {memory_usage}%..."
    
    # Sends via Gmail SMTP
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
```
This function **only runs if email alerts are enabled**.

**4. GET TOP PROCESSES Function (Lines 86-105)**
```python
def get_top_processes(n=3):
    processes = []
    for proc in psutil.process_iter([...]):
        # Collects all running processes
        processes.append({...})
    
    # Sort and return top 3
    return sorted(processes, ...)[:3]
```
Gets the **3 apps using the most CPU**.

**5. MAIN LOOP (Lines 107-157)**
```python
while True:
    # Get metrics (every 5 seconds)
    cpu_usage = psutil.cpu_percent()      # Get current CPU %
    memory_usage = psutil.virtual_memory().percent   # Get Memory %
    disk_usage = psutil.disk_usage('/').percent      # Get Disk %
    
    # Log them
    logger.info(f"CPU: {cpu_usage}% | Memory: {memory_usage}% | Disk: {disk_usage}%")
    
    # If CPU > 80%, check cooldown and send alert
    if cpu_usage > THRESHOLD:
        if time_since_last_alert > 5_minutes:
            logger.warning(f"ALERT! CPU is {cpu_usage}%")
            send_email_alert(...)
    
    time.sleep(5)  # Wait 5 seconds before next check
```
This is the **heart** of the monitor:
1. Grabs 3 metrics
2. Logs them
3. If CPU is high + enough time passed, sends alert
4. Repeats every 5 seconds

---

### Overview
The `system_monitor.py` service continuously monitors system-wide **CPU, memory, and disk** usage. It sends alerts when CPU usage exceeds 80%.

### Features

✅ **Real-time Monitoring**
- Checks CPU, Memory, and Disk every 5 seconds
- Identifies top 3 processes consuming CPU
- Tracks all system metrics in one place

✅ **Advanced Logging**
- Structured logs with timestamps
- File logging (`system_monitor.log`) + console output
- Different severity levels (INFO, WARNING, ERROR)

✅ **Smart Alerts**
- Alert cooldown (5 minutes) to prevent alert spam
- Alert counter to track alert history
- Shows which processes are hogging CPU

✅ **BONUS: Email Alerts** (Optional)
- Sends email notifications when CPU exceeds threshold
- Includes detailed metrics and top processes
- Uses Gmail SMTP (or any SMTP server)

### Architecture & Implementation

**How it works:**
```
1. Start monitoring loop
2. Every 5 seconds:
   - Get current CPU/Memory/Disk usage (SYSTEM-WIDE)
   - Get top 3 processes by CPU usage
   - Log all metrics
   - If CPU > 80%:
     - Check if enough time has passed since last alert (cooldown)
     - If yes: Send alert (logging + optional email)
     - If no: Skip this alert (prevent spam)
3. Repeat
```

**What it monitors (System-wide):**

| Metric | What it means | Example |
|--------|---------------|---------|
| CPU | Total processor usage across all apps | 45% - all processes combined |
| Memory | Total RAM in use | 32% - across all running apps |
| Disk | Total storage in use | 60% - entire system disk |
| Top Processes | Individual apps using most CPU | Python (15%), RabbitMQ (8%), etc. |

**Key Components:**

| Component | Purpose |
|-----------|---------|
| `psutil` | Gets system-wide and process metrics |
| `logging` | Structured logging to file and console |
| `smtplib` | Sends email alerts (optional) |
| `cooldown` | Prevents alert spam (5 min between alerts) |
| `top_processes` | Shows which apps are using CPU |

### Running the System Monitor

**Option 1: Via Docker Compose (included)**
```bash
docker-compose up
```

The System Monitor runs automatically in its container and logs everything.

**Option 2: Standalone (on your machine)**
```bash
python system_monitor.py
```

**Option 3: With Email Alerts Enabled**
```bash
export SEND_EMAIL_ALERTS=true
export EMAIL_FROM=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password  # Use App Password for Gmail
export EMAIL_TO=recipient@gmail.com
python system_monitor.py
```

### Email Alert Setup (Gmail)

1. **Enable 2-Factor Authentication** on Gmail
2. **Create an App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
3. **Set environment variables:**
   ```bash
   export EMAIL_FROM=your-email@gmail.com
   export EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # 16-char app password
   export EMAIL_TO=recipient@gmail.com
   export SEND_EMAIL_ALERTS=true
   ```
4. **Run the monitor:**
   ```bash
   python system_monitor.py
   ```

### Example Output

**Console/Log Output:**
```
2024-01-31 10:15:00,123 - INFO - ============================================================
2024-01-31 10:15:00,124 - INFO - System Monitor Service Started
2024-01-31 10:15:00,124 - INFO - Monitoring: CPU, Memory, Disk
2024-01-31 10:15:00,124 - INFO - CPU Threshold: 80%
2024-01-31 10:15:00,125 - INFO - ============================================================
2024-01-31 10:15:01,234 - INFO - 📊 CPU:  45.2% | Memory:  32.1% | Disk:  60.5%
2024-01-31 10:15:06,456 - INFO - 📊 CPU:  52.3% | Memory:  33.5% | Disk:  60.5%
2024-01-31 10:15:11,789 - WARNING - 🚨 ALERT #1: CPU usage is 85.6% (threshold: 80%)
2024-01-31 10:15:11,790 - WARNING -    Top processes: python (28.5%), chrome (15.2%), docker (8.1%)
2024-01-31 10:15:11,850 - INFO - ✉️ Email alert sent to recipient@gmail.com
```

**Email Alert Example:**
```
Subject: ⚠️ HIGH CPU ALERT: 85.6% usage detected

HIGH CPU USAGE ALERT
===================

Current Metrics:
- CPU Usage: 85.6%
- Memory Usage: 33.5%
- Threshold: 80%
- Timestamp: 2024-01-31 10:15:11

Top CPU-consuming processes:
1. python - 28.5% CPU, 12.1% Memory
2. chrome - 15.2% CPU, 8.5% Memory
3. docker - 8.1% CPU, 5.2% Memory
```

### Customization

Edit `system_monitor.py` to change:
- **THRESHOLD**: CPU alert level (currently 80%)
- **CHECK_INTERVAL**: How often to check (currently 5 seconds)
- **ALERT_COOLDOWN**: Minimum time between alerts (currently 5 minutes)

### How to View and Understand Logs

**Option 1: View logs in real-time from Docker**
```bash
docker logs -f system_monitor
```
The `-f` means "follow" - shows new logs as they appear.

**Option 2: View saved log file**
```bash
# If running locally
tail -f system_monitor.log

# If in Docker, copy the log out
docker cp system_monitor:/app/system_monitor.log .
cat system_monitor.log
```

**Option 3: View only warnings/alerts**
```bash
docker logs system_monitor | grep "ALERT\|WARNING"
```

### Understanding the Log Output

**Normal operation:**
```
2024-01-31 10:15:01 - INFO - 📊 CPU:  45.2% | Memory:  32.1% | Disk:  60.5%
2024-01-31 10:15:06 - INFO - 📊 CPU:  52.3% | Memory:  33.5% | Disk:  60.5%
```
✅ Everything normal, metrics logged every 5 seconds

**High CPU detected:**
```
2024-01-31 10:15:11 - WARNING - 🚨 ALERT #1: CPU usage is 85.6% (threshold: 80%)
2024-01-31 10:15:11 - WARNING -    Top processes: python (28.5%), chrome (15.2%), docker (8.1%)
2024-01-31 10:15:12 - INFO - ✉️ Email alert sent to recipient@gmail.com
```
⚠️ CPU exceeded threshold, alert sent (if email enabled)

**After 5 minutes:**
```
2024-01-31 10:20:15 - WARNING - 🚨 ALERT #2: CPU usage is 82.1% (threshold: 80%)
2024-01-31 10:20:15 - WARNING -    Top processes: docker (18.5%), python (12.3%), node (5.1%)
2024-01-31 10:20:16 - INFO - ✉️ Email alert sent to recipient@gmail.com
```
✅ Another alert sent (only after 5-minute cooldown passed)

### Log File

Logs are saved to `system_monitor.log` with full details:
```bash
tail -f system_monitor.log  # Watch logs in real-time
```

---

## Project Structure

- `publisher.py` - Sends 10 messages to "ABC" queue + bonus interactive mode
- `consumer.py` - Listens to "ABC" queue and prints messages
- `system_monitor.py` - Monitors CPU/Memory/Disk usage with advanced logging and email alerts
- `docker-compose.yml` - Orchestrates all services
- `Dockerfile.publisher`, `Dockerfile.consumer`, `Dockerfile.cpu` - Container configurations
- `system_monitor.log` - Generated log file from system monitor
