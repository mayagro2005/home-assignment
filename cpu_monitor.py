import psutil
import time

THRESHOLD = 80  # CPU usage threshold in percent

print("CPU Monitor started. Checking every 5 seconds...")

while True:
    cpu = psutil.cpu_percent(interval=1)
    print("CPU Usage:", cpu, "%")

    if cpu > THRESHOLD:
        print("ALERT! CPU usage too high:", cpu)

    time.sleep(5)
