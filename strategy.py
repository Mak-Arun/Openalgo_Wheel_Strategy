# strategy.py

from utils import send_telegram_alert, get_option_symbol, get_nearest_expiry, Session, Position
from datetime import datetime
import time

def get_spot_price(client, symbol):
    quote = client.quotes(symbol=symbol, exchange="NSE")
    return quote['data']['ltp']

def is_option_valid(client, symbol):
    try:
        quote = client.quotes(symbol=symbol, exchange="NFO")
        ltp = quote['data']['ltp']
        return ltp >= 10, ltp
    except:
        return False, 0

def place_option_with_sl(client, base_symbol, expiry, strike, opt_type, qty):
    sym = get_option_symbol(base_symbol, expiry, strike, opt_type)
    valid, price = is_option_valid(client, sym)
    if not valid:
        send_telegram_alert(f"❌ Skipped *{sym}* — Premium < ₹10")
        return

    order = client.placeorder(strategy="wheel", symbol=sym, action="SELL", exchange="NFO",
                              price_type="MARKET", product="MIS", quantity=qty)
    send_telegram_alert(f"✅ *{sym}* Sold @ ₹{price}\nQty: {qty}")

    # SL = 30% higher
    sl_price = round(price * 1.3, 1)
    trig = round(sl_price - 0.5, 1)

    sl = client.placeorder(strategy="wheel", symbol=sym, action="BUY", exchange="NFO",
                           price_type="SL", product="MIS", quantity=qty,
                           price=sl_price, trigger_price=trig)
    send_telegram_alert(f"🔒 SL for *{sym}* @ ₹{sl_price} (Trig ₹{trig})")

def run_wheel_strategy_for_symbol(client, symbol, quantity):
    session = Session()
    spot = get_spot_price(client, symbol)
    strike = round(spot / 10) * 10
    expiry = get_nearest_expiry(client, symbol)

    last_pos = session.query(Position).filter_by(symbol=symbol).order_by(Position.timestamp.desc()).first()

    if not last_pos or (not last_pos.has_stock and last_pos.last_action == "SELL_CALL"):
        place_option_with_sl(client, symbol, expiry, strike, "PE", quantity)
        session.add(Position(symbol=symbol, has_stock=False, last_action="SELL_PUT", timestamp=datetime.now()))
    elif last_pos.has_stock and last_pos.last_action == "SELL_PUT":
        place_option_with_sl(client, symbol, expiry, strike, "CE", quantity)
        session.add(Position(symbol=symbol, has_stock=True, last_action="SELL_CALL", timestamp=datetime.now()))

    session.commit()
    session.close()
