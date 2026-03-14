"""Basic, scalable algo trading agent package."""

from trading_agent.backtest import BacktestEngine, BacktestResult
from trading_agent.strategy import StrategyConfig, TechnicalStrategy, TraderMode

__all__ = [
    "BacktestEngine",
    "BacktestResult",
    "StrategyConfig",
    "TechnicalStrategy",
    "TraderMode",
]
