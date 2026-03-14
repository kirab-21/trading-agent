from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import List

from trading_agent.indicators import atr, ema, rsi
from trading_agent.models import Candle, Position, Signal, Trade
from trading_agent.strategy import TechnicalStrategy


@dataclass
class BacktestResult:
    initial_capital: float
    final_capital: float
    total_return_pct: float
    max_drawdown_pct: float
    win_rate_pct: float
    total_trades: int
    avg_trade_return_pct: float
    trades: List[Trade]


class BacktestEngine:
    def __init__(
        self,
        strategy: TechnicalStrategy,
        transaction_cost_pct: float = 0.001,
        slippage_pct: float = 0.0005,
    ):
        self.strategy = strategy
        self.transaction_cost_pct = transaction_cost_pct
        self.slippage_pct = slippage_pct

    def run(self, symbol: str, candles: List[Candle], initial_capital: float) -> BacktestResult:
        if len(candles) < max(self.strategy.config.slow_ema, self.strategy.config.atr_period) + 5:
            raise ValueError("Not enough candles for selected indicator periods")

        closes = [c.close for c in candles]
        highs = [c.high for c in candles]
        lows = [c.low for c in candles]

        fast_ema_values = ema(closes, self.strategy.config.fast_ema)
        slow_ema_values = ema(closes, self.strategy.config.slow_ema)
        rsi_values = rsi(closes, self.strategy.config.rsi_period)
        atr_values = atr(highs, lows, closes, self.strategy.config.atr_period)

        cash = initial_capital
        equity_curve: List[float] = []
        current_position: Position | None = None
        position_bars_held = 0
        trades: List[Trade] = []

        for i, candle in enumerate(candles):
            close = candle.close
            current_equity = cash + ((current_position.quantity * close) if current_position else 0.0)
            equity_curve.append(current_equity)

            if i == 0:
                continue

            previous_candle = candles[i - 1]

            if current_position is not None:
                position_bars_held += 1

            if (
                current_position is not None
                and self.strategy.config.force_exit_end_of_day
                and candle.timestamp.date() != previous_candle.timestamp.date()
            ):
                cash, trades = self._close_position(
                    current_position=current_position,
                    exit_candle=candle,
                    cash=cash,
                    trades=trades,
                )
                current_position = None
                position_bars_held = 0
                continue

            stop_loss = current_position.stop_loss if current_position else None
            take_profit = current_position.take_profit if current_position else None
            signal = self.strategy.get_signal(
                fast_ema_value=fast_ema_values[i],
                slow_ema_value=slow_ema_values[i],
                rsi_value=rsi_values[i],
                in_position=current_position is not None,
                close_price=close,
                stop_loss=stop_loss,
                take_profit=take_profit,
                bars_held=position_bars_held,
            )

            if signal == Signal.BUY and current_position is None:
                atr_value = max(atr_values[i], 0.01)
                raw_entry_price = close * (1 + self.slippage_pct)
                stop = raw_entry_price - self.strategy.config.stop_atr_multiple * atr_value
                take = raw_entry_price + self.strategy.config.take_profit_atr_multiple * atr_value
                qty = self.strategy.position_size(cash, raw_entry_price, stop)

                if qty > 0:
                    gross = qty * raw_entry_price
                    cost = gross * self.transaction_cost_pct
                    total_buy = gross + cost
                    if total_buy <= cash:
                        cash -= total_buy
                        current_position = Position(
                            symbol=symbol,
                            quantity=qty,
                            avg_price=raw_entry_price,
                            entry_time=candle.timestamp,
                            stop_loss=stop,
                            take_profit=take,
                        )
                        position_bars_held = 0

            elif signal == Signal.SELL and current_position is not None:
                cash, trades = self._close_position(
                    current_position=current_position,
                    exit_candle=candle,
                    cash=cash,
                    trades=trades,
                )
                current_position = None
                position_bars_held = 0

        if current_position is not None:
            cash, trades = self._close_position(
                current_position=current_position,
                exit_candle=candles[-1],
                cash=cash,
                trades=trades,
            )

        final_capital = cash
        total_return_pct = ((final_capital / initial_capital) - 1) * 100
        max_drawdown_pct = self._max_drawdown(equity_curve)
        wins = [t for t in trades if t.pnl > 0]
        win_rate_pct = (len(wins) / len(trades) * 100) if trades else 0.0
        avg_trade_return_pct = mean([t.return_pct for t in trades]) if trades else 0.0

        return BacktestResult(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return_pct=total_return_pct,
            max_drawdown_pct=max_drawdown_pct,
            win_rate_pct=win_rate_pct,
            total_trades=len(trades),
            avg_trade_return_pct=avg_trade_return_pct,
            trades=trades,
        )

    def _close_position(
        self,
        current_position: Position,
        exit_candle: Candle,
        cash: float,
        trades: List[Trade],
    ) -> tuple[float, List[Trade]]:
        raw_exit_price = exit_candle.close * (1 - self.slippage_pct)
        gross = current_position.quantity * raw_exit_price
        cost = gross * self.transaction_cost_pct
        cash += gross - cost

        pnl = (raw_exit_price - current_position.avg_price) * current_position.quantity
        pnl -= current_position.avg_price * current_position.quantity * self.transaction_cost_pct
        pnl -= cost
        trade_return_pct = (raw_exit_price / current_position.avg_price - 1) * 100

        trades.append(
            Trade(
                symbol=current_position.symbol,
                entry_time=current_position.entry_time,
                exit_time=exit_candle.timestamp,
                entry_price=current_position.avg_price,
                exit_price=raw_exit_price,
                quantity=current_position.quantity,
                pnl=pnl,
                return_pct=trade_return_pct,
            )
        )
        return cash, trades

    @staticmethod
    def _max_drawdown(equity_curve: List[float]) -> float:
        if not equity_curve:
            return 0.0

        peak = equity_curve[0]
        max_dd = 0.0
        for eq in equity_curve:
            peak = max(peak, eq)
            drawdown = (peak - eq) / peak if peak else 0.0
            max_dd = max(max_dd, drawdown)

        return max_dd * 100
