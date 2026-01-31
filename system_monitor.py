import psutil
import time
import logging
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
THRESHOLD = 80
CHECK_INTERVAL = 5
ALERT_COOLDOWN = 300

# ==================== LOGGING SETUP ====================
LOG_DIR = "/logs"
LOG_FILE = os.path.join(LOG_DIR, "system_monitor.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Create handlers
file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
console_handler = logging.StreamHandler()

# Set formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ==================== ALERT TRACKING ====================
last_alert_time = 0
alert_count = 0

# ==================== PROCESS UTILS ====================
def get_top_processes(n=3):
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            processes.append({
                "name": proc.info["name"],
                "cpu": proc.info["cpu_percent"]
            })
        except:
            pass

    return sorted(processes, key=lambda x: x["cpu"], reverse=True)[:n]

# ==================== MAIN LOOP ====================
def main():
    global last_alert_time, alert_count

    logger.info("=" * 60)
    logger.info("System Monitor Started")
    logger.info(f"Threshold: {THRESHOLD}%")
    logger.info(f"Interval: {CHECK_INTERVAL}s")
    logger.info("=" * 60)

    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            logger.info(f"CPU: {cpu}% | MEM: {mem}% | DISK: {disk}%")

            if cpu > THRESHOLD:
                now = time.time()
                if now - last_alert_time > ALERT_COOLDOWN:
                    alert_count += 1
                    last_alert_time = now

                    top = get_top_processes()
                    logger.warning(f"ALERT #{alert_count} CPU {cpu}%")
                    logger.warning("Top processes:")
                    for p in top:
                        logger.warning(f" - {p['name']} ({p['cpu']}%)")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
