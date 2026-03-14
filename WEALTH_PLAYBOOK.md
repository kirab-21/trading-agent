# Wealth Playbook for This Trading Agent

> This is a risk-managed process guide, not a return guarantee.

## 1) Mindset: Wealth comes from process + survival

If your goal is wealth generation, focus on:

- capital preservation first,
- consistent positive expectancy,
- controlled compounding,
- strict drawdown control.

A strategy that survives for years can compound. A strategy that blows up cannot.

## 2) Pick one style and stay consistent

This project supports:

- `swing` mode (multi-day holding)
- `daily` mode (faster, frequent exits)

Do not mix styles randomly. Pick one mode, evaluate it for 3-6 months, and improve only in scheduled review windows.

## 3) Suggested capital allocation framework

For your total investable capital, start like this:

- 70-90%: passive core (index funds / long-term investing)
- 10-30%: active strategy capital (this agent)

Within active strategy capital:

- risk only **0.5% to 1.0%** per trade,
- set hard max daily loss,
- cap total deployed capital per day.

## 4) Compounding rules (practical)

- Start with fixed base capital for first 30-50 trades.
- Increase size only after:
  - positive expectancy,
  - acceptable drawdown,
  - stable execution quality.
- Scale in steps (e.g. +10-15%), not all at once.
- If drawdown breaches threshold, auto-decrease size.

## 5) Backtesting workflow before trusting results

1. Use multi-year data.
2. Split into in-sample and out-of-sample.
3. Test realistic costs + slippage.
4. Avoid overfitting (too many parameter tweaks).
5. Compare modes and keep one for live pilot.

## 6) Paper trade -> small live -> scale

A safer rollout:

1. Backtest complete.
2. Paper trade 2-4 weeks.
3. Live with small capital.
4. Scale only after consistent monthly performance.

## 7) Metrics you should track weekly

- Net return.
- Max drawdown.
- Win rate.
- Average win / average loss.
- Expectancy per trade.
- Slippage vs modeled slippage.
- Strategy adherence (did you override system manually?).

## 8) Example monthly review checklist

- Is drawdown within plan?
- Is realized slippage close to backtest assumptions?
- Are returns concentrated in few trades or broad-based?
- Any regime change (trending vs choppy market)?
- Keep / reduce / pause / retune?

## 9) Non-negotiable risk controls

- Stop trading after max daily loss breach.
- Pause strategy after severe drawdown.
- No revenge trading / manual impulse overrides.
- Keep audit trail of every signal and order.

## 10) How to apply with this repo

1. Run both modes on your data:

```bash
python run_backtest.py --csv <your_data.csv> --symbol <SYMBOL> --mode swing
python run_backtest.py --csv <your_data.csv> --symbol <SYMBOL> --mode daily
```

2. Pick one mode using objective metrics.
3. Set risk using `--risk` (start low, e.g. `0.005` to `0.01`).
4. Go through deployment steps in `DEPLOYMENT.md`.
5. Scale only after evidence, not emotions.

## 11) Reality check

There is no guaranteed “wealth mode.”

Your edge comes from:

- disciplined execution,
- risk management,
- continuous measurement,
- and long-term consistency.
