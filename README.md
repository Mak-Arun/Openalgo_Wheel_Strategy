# OpenAlgo Dynamic Wheel Strategy (Multi-Symbol)

A production-ready Python bot to execute a Dynamic Wheel Options Strategy for multiple stocks using [OpenAlgo](https://openalgo.in) API.

## 🚀 Features
- ✅ Multi-symbol support (SBIN, RELIANCE, etc)
- ✅ Nearest expiry detection from live option chain
- ✅ Entry order + SL (30% over premium)
- ✅ Telegram alerts on entry & SL
- ✅ SQLite DB logging using SQLAlchemy
- ✅ Scheduled via APScheduler in IST

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/openalgo-dynamic-wheel-strategy.git
cd openalgo-dynamic-wheel-strategy
