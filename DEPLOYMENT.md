# Deployment Guide (Paper -> Live)

This guide explains how to take the current algo-trading code from local backtests to a deployable setup.

## 1) Local setup

```bash
cd /workspace/trading-agent
python -m venv .venv
source .venv/bin/activate
python --version
```

No third-party package is required for the current code (pure stdlib).

## 2) Backtest workflow (recommended before any deployment)

### 2.1 Prepare your CSV

The CSV must have:

```text
datetime,open,high,low,close,volume
```

### 2.2 Run swing backtest

```bash
python run_backtest.py --csv data/sample_nse_stock.csv --symbol RELIANCE.NS --mode swing
```

### 2.3 Run daily backtest

```bash
python run_backtest.py --csv data/sample_nse_stock.csv --symbol RELIANCE.NS --mode daily
```

### 2.4 Override parameters

```bash
python run_backtest.py \
  --csv data/sample_nse_stock.csv \
  --symbol RELIANCE.NS \
  --mode swing \
  --capital 500000 \
  --risk 0.008 \
  --fast-ema 13 \
  --slow-ema 34 \
  --rsi-buy-threshold 57
```

## 3) Recommended path to deploy safely

1. **Backtest** on at least 3-5 years of historical data.
2. **Paper trade** for 2-4 weeks with live market feed and simulated orders.
3. **Start small live capital** (strict risk limits).
4. Add monitoring + kill switch.

## 4) Integrate your Indian broker

Implement `Broker` methods in `trading_agent/broker.py` with your broker API:

- `buy(symbol, qty, price)`
- `sell(symbol, qty, price)`

Keep strategy/backtest logic unchanged.

## 5) Live execution architecture (minimum)

- **Data fetcher**: pull latest candles from broker/data provider.
- **Signal engine**: compute indicators and call `TechnicalStrategy.get_signal`.
- **Risk manager**: position sizing and max daily loss checks.
- **Order executor**: place orders via your `Broker` implementation.
- **Journal/logging**: store all signals/orders/trades.

## 6) VPS deployment outline (Ubuntu)

### 6.1 Server bootstrap

```bash
sudo apt update
sudo apt install -y python3 python3-venv git
```

### 6.2 Clone and configure

```bash
git clone <your-repo-url> trading-agent
cd trading-agent
python3 -m venv .venv
source .venv/bin/activate
```

### 6.3 Run your live runner with systemd

Create `/etc/systemd/system/trading-agent.service` (example):

```ini
[Unit]
Description=Trading Agent Live Runner
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading-agent
ExecStart=/home/ubuntu/trading-agent/.venv/bin/python run_live.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable trading-agent
sudo systemctl start trading-agent
sudo systemctl status trading-agent
```

> `run_live.py` is your live-loop entrypoint once broker integration is complete.

## 7) Production risk controls (must-have)

- Max daily loss cap (stop trading for day).
- Max open positions / max capital deployed.
- Per-trade risk cap.
- Exchange session/time guard.
- Circuit-breaker on repeated API failures.
- Alerting (Telegram/Slack/Email).

## 8) What to monitor

- Open positions.
- Fill success rate / rejection rate.
- Slippage vs expected.
- Latency of market data and order placement.
- Daily and rolling PnL.

## 9) Common mistakes to avoid

- Going live directly after one backtest run.
- Ignoring brokerage/charges and slippage.
- Overfitting strategy parameters.
- Not logging rejected orders and API errors.
