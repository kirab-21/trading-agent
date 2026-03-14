from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from trading_agent.models import Signal


class TraderMode(str, Enum):
    DAILY = "daily"
    SWING = "swing"


@dataclass
class StrategyConfig:
    fast_ema: int = 20
    slow_ema: int = 50
    rsi_period: int = 14
    rsi_buy_threshold: float = 55.0
    rsi_sell_threshold: float = 45.0
    atr_period: int = 14
    stop_atr_multiple: float = 2.0
    take_profit_atr_multiple: float = 3.0
    risk_per_trade: float = 0.01
    force_exit_end_of_day: bool = False
    max_holding_bars: int | None = None

    @classmethod
    def from_mode(cls, mode: TraderMode) -> "StrategyConfig":
        if mode == TraderMode.DAILY:
            # Daily trader / intraday-like profile: faster reaction + same-day exit.
            return cls(
                fast_ema=9,
                slow_ema=21,
                rsi_period=14,
                rsi_buy_threshold=58.0,
                rsi_sell_threshold=48.0,
                atr_period=14,
                stop_atr_multiple=1.5,
                take_profit_atr_multiple=2.0,
                risk_per_trade=0.005,
                force_exit_end_of_day=True,
                max_holding_bars=24,
            )

        # Swing trader profile: slower trend following, multi-day holding.
        return cls(
            fast_ema=20,
            slow_ema=50,
            rsi_period=14,
            rsi_buy_threshold=55.0,
            rsi_sell_threshold=45.0,
            atr_period=14,
            stop_atr_multiple=2.0,
            take_profit_atr_multiple=3.0,
            risk_per_trade=0.01,
            force_exit_end_of_day=False,
            max_holding_bars=None,
        )


class TechnicalStrategy:
    """Simple trend-following + momentum filter strategy for long-only investing."""

    def __init__(self, config: StrategyConfig):
        self.config = config

    def get_signal(
        self,
        fast_ema_value: float,
        slow_ema_value: float,
        rsi_value: float,
        in_position: bool,
        close_price: float,
        stop_loss: float | None,
        take_profit: float | None,
        bars_held: int = 0,
    ) -> Signal:
        if in_position and self.config.max_holding_bars is not None and bars_held >= self.config.max_holding_bars:
            return Signal.SELL

        if in_position and stop_loss is not None and close_price <= stop_loss:
            return Signal.SELL

        if in_position and take_profit is not None and close_price >= take_profit:
            return Signal.SELL

        bullish_trend = fast_ema_value > slow_ema_value
        bearish_trend = fast_ema_value < slow_ema_value

        if not in_position and bullish_trend and rsi_value >= self.config.rsi_buy_threshold:
            return Signal.BUY

        if in_position and bearish_trend and rsi_value <= self.config.rsi_sell_threshold:
            return Signal.SELL

        return Signal.HOLD

    def position_size(self, capital: float, entry_price: float, stop_loss: float) -> int:
        risk_amount = capital * self.config.risk_per_trade
        per_share_risk = max(entry_price - stop_loss, 0.01)
        qty = int(risk_amount / per_share_risk)
        max_affordable = int(capital / entry_price)
        return max(min(qty, max_affordable), 0)
