from __future__ import annotations

import argparse

from trading_agent.backtest import BacktestEngine
from trading_agent.data import load_candles_from_csv
from trading_agent.strategy import StrategyConfig, TechnicalStrategy, TraderMode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run backtest for technical strategy")
    parser.add_argument("--csv", required=True, help="Path to OHLCV CSV")
    parser.add_argument("--symbol", required=True, help="Symbol name (e.g., RELIANCE.NS)")
    parser.add_argument("--mode", choices=[m.value for m in TraderMode], default=TraderMode.SWING.value)
    parser.add_argument("--capital", type=float, default=200000.0, help="Initial capital")
    parser.add_argument("--risk", type=float, default=None, help="Override risk per trade (0-1)")
    parser.add_argument("--fast-ema", type=int, default=None)
    parser.add_argument("--slow-ema", type=int, default=None)
    parser.add_argument("--rsi-buy-threshold", type=float, default=None)
    parser.add_argument("--transaction-cost-pct", type=float, default=0.001)
    parser.add_argument("--slippage-pct", type=float, default=0.0005)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mode = TraderMode(args.mode)

    config = StrategyConfig.from_mode(mode)

    if args.fast_ema is not None:
        config.fast_ema = args.fast_ema
    if args.slow_ema is not None:
        config.slow_ema = args.slow_ema
    if args.rsi_buy_threshold is not None:
        config.rsi_buy_threshold = args.rsi_buy_threshold
    if args.risk is not None:
        config.risk_per_trade = args.risk

    strategy = TechnicalStrategy(config)
    engine = BacktestEngine(
        strategy=strategy,
        transaction_cost_pct=args.transaction_cost_pct,
        slippage_pct=args.slippage_pct,
    )

    candles = load_candles_from_csv(args.csv)
    result = engine.run(symbol=args.symbol, candles=candles, initial_capital=args.capital)

    print("=" * 60)
    print(f"Backtest Result for {args.symbol}")
    print(f"Mode: {mode.value}")
    print("=" * 60)
    print(f"Initial Capital     : {result.initial_capital:,.2f}")
    print(f"Final Capital       : {result.final_capital:,.2f}")
    print(f"Total Return %      : {result.total_return_pct:.2f}%")
    print(f"Max Drawdown %      : {result.max_drawdown_pct:.2f}%")
    print(f"Total Trades        : {result.total_trades}")
    print(f"Win Rate %          : {result.win_rate_pct:.2f}%")
    print(f"Avg Trade Return %  : {result.avg_trade_return_pct:.2f}%")

    if result.trades:
        last_trade = result.trades[-1]
        print("-" * 60)
        print("Last trade snapshot:")
        print(
            f"Entry={last_trade.entry_time} @ {last_trade.entry_price:.2f}, "
            f"Exit={last_trade.exit_time} @ {last_trade.exit_price:.2f}, "
            f"PnL={last_trade.pnl:.2f}"
        )


if __name__ == "__main__":
    main()
