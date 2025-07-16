# utils.py

import os
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil import parser

load_dotenv()

# Telegram Config
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine("sqlite:///wheel_strategy.db")
Session = sessionmaker(bind=engine)

# Telegram Alerts
def send_telegram_alert(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"📣 OpenAlgo:\n\n{message}", "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Nearest Expiry Detector
def get_nearest_expiry(client, symbol: str, exchange: str = "NFO") -> str:
    try:
        chain = client.optionchain(symbol=symbol, exchange=exchange)
        expiries = chain.get("expiries", [])
        dates = sorted([parser.parse(e) for e in expiries])
        formatted = dates[0].strftime("%d%b%y").upper()
        send_telegram_alert(f"📅 {symbol}: Nearest Expiry → *{formatted}*")
        return formatted
    except Exception as e:
        print(f"⚠️ Expiry fetch failed: {e}")
        return datetime.now().strftime("%d%b%y").upper()

# Option Symbol Formatter
def get_option_symbol(base: str, expiry: str, strike: int, opt_type: str) -> str:
    return f"{base}{expiry}{strike}{opt_type}"

# DB Position Table
class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    has_stock = Column(Boolean)
    last_action = Column(String)
    timestamp = Column(DateTime)

Base.metadata.create_all(engine)
