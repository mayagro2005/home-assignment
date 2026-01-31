import psutil
import time
import logging
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================== CONFIGURATION ====================
THRESHOLD = 80
CHECK_INTERVAL = 5
ALERT_COOLDOWN = 300

# Email configuration
SEND_EMAIL_ALERTS = os.getenv('SEND_EMAIL_ALERTS', 'False').lower() == 'true'
EMAIL_FROM = os.getenv('EMAIL_FROM', 'your-email@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_TO = os.getenv('EMAIL_TO', 'your-email@gmail.com')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# ==================== LOGGING SETUP ====================
LOG_DIR = "/logs"
LOG_FILE = os.path.join(LOG_DIR, "system_monitor.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ==================== ALERT TRACKING ====================
last_alert_time = 0
alert_count = 0

# ==================== EMAIL ALERT FUNCTION ====================
def send_email_alert(cpu_usage, memory_usage, top_processes):
    try:
        if not SEND_EMAIL_ALERTS or not EMAIL_PASSWORD:
            return False

        subject = f"HIGH CPU ALERT: {cpu_usage}%"

        body = f"""
HIGH CPU USAGE ALERT
===================

CPU Usage: {cpu_usage}%
Memory Usage: {memory_usage}%
Threshold: {THRESHOLD}%
Time: {datetime.now()}

Top processes:
"""
        for i, proc in enumerate(top_processes, 1):
            body += f"\n{i}. {proc['name']} - {proc['cpu']}% CPU"

        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email alert sent to {EMAIL_TO}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")
        return False

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
    logger.info(f"Email alerts: {'ON' if SEND_EMAIL_ALERTS else 'OFF'}")
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

                    send_email_alert(cpu, mem, top)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
