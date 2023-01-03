from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from status import get_status
from update import get_update, send_error_message
from config import print_n_log
import psutil

def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_update, "interval", minutes=30, next_run_time=datetime.now())
    scheduler.start()
    get_status()

if __name__ == "__main__":
    main()