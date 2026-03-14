# Basic Indian Market Algo Trading Agent

A minimal, scalable Python codebase for:

- Technical-indicator based signal generation.
- Rule-based execution logic.
- Backtesting on your own OHLCV CSV data.
- A paper-broker interface that can later be swapped with a real broker API.

## What this project gives you

- **Business logic only** (no hard-coupled broker dependency).
- **Two trading styles out of the box**:
  - `swing`: multi-day trend-following profile.
  - `daily`: fast profile with end-of-day position exit logic.
- **Backtesting engine** with transaction cost + slippage modeling.
- **Modular design** so you can extend over time.

## Project structure

- `trading_agent/models.py` - Market data and trade models.
- `trading_agent/indicators.py` - Technical indicators (EMA, RSI, ATR).
- `trading_agent/strategy.py` - Signal/risk logic + daily/swing presets.
- `trading_agent/backtest.py` - Backtesting engine and metrics.
- `trading_agent/data.py` - CSV loader for OHLCV candles.
- `trading_agent/broker.py` - Broker abstraction + paper broker.
- `run_backtest.py` - CLI entrypoint for backtest.

## CSV format expected

Header must include:

```text
datetime,open,high,low,close,volume
```

`datetime` should be in ISO-like format (for example: `2024-01-01 09:15:00`).

## Quick start

### Swing trader mode (default)

```bash
python run_backtest.py --csv data/reliance_1d.csv --symbol RELIANCE.NS --mode swing
```

### Daily trader mode

```bash
python run_backtest.py --csv data/reliance_1d.csv --symbol RELIANCE.NS --mode daily
```

Optional overrides:

```bash
python run_backtest.py \
  --csv data/reliance_1d.csv \
  --symbol RELIANCE.NS \
  --mode swing \
  --capital 500000 \
  --risk 0.01 \
  --fast-ema 20 \
  --slow-ema 50 \
  --rsi-buy-threshold 55
```

## Notes for Indian market usage

- Set realistic **brokerage + charges** via `transaction_cost_pct` in backtest.
- Respect lot sizes / tick sizes if you move to derivatives.
- For intraday deployment, apply exchange timing constraints and hard square-off rules in your live executor.
- For live deployment, implement `Broker` against your broker API and reuse `TechnicalStrategy` + risk logic.

## Next scaling steps

1. Add multi-symbol portfolio allocator.
2. Add walk-forward optimization.
3. Add paper/live scheduler (15m/day candles).
4. Add structured logging + monitoring.
5. Add persistent trade journal (SQLite/Postgres).
