# main.py

from apscheduler.schedulers.background import BackgroundScheduler
from openalgo import api
from strategy import run_wheel_strategy_for_symbol
from dotenv import load_dotenv
import os
import time
from pytz import timezone

load_dotenv()

API_KEY = os.getenv("OPENALGO_API_KEY")
API_HOST = os.getenv("OPENALGO_API_HOST")
SYMBOLS = os.getenv("STOCK_SYMBOLS").split(",")
QTY = int(os.getenv("QUANTITY", 1))

client = api(api_key=API_KEY, host=API_HOST)

def schedule_for_all():
    for symbol in SYMBOLS:
        run_wheel_strategy_for_symbol(client, symbol.strip(), QTY)

if __name__ == '__main__':
    print("🔁 OpenAlgo Python Bot is running.")
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(schedule_for_all, 'cron', day_of_week='mon-fri', hour=9, minute=45)
    scheduler.start()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
