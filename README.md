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
- `DEPLOYMENT.md` - step-by-step deployment runbook.

## CSV format expected

Header must include:

```text
datetime,open,high,low,close,volume
```

`datetime` should be in ISO-like format (for example: `2024-01-01 09:15:00`).

## What to do (quick path)

1. Prepare CSV data for your NSE/BSE symbol.
2. Run backtest in `swing` and `daily` mode.
3. Tune risk and indicator params.
4. Validate on out-of-sample data.
5. Start paper trading.
6. Deploy live with strict risk controls.

## How to run it

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

## How to backtest properly

- Use realistic costs (`--transaction-cost-pct`) and slippage (`--slippage-pct`).
- Test on multi-year data.
- Keep separate train/test time periods.
- Compare both modes and keep the one matching your timeframe.


## How to use it to generate wealth (practically)

Read and follow **[WEALTH_PLAYBOOK.md](WEALTH_PLAYBOOK.md)**.

It gives a concrete framework for:

- risk-first capital allocation,
- compounding without over-sizing,
- backtest -> paper -> live progression,
- and review metrics to scale safely.

## How to deploy

Deployment plan is documented in:

- **[DEPLOYMENT.md](DEPLOYMENT.md)**

It includes:

- local setup,
- broker integration approach,
- VPS + `systemd` deployment pattern,
- monitoring and risk checklist.

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
