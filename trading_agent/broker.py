from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from trading_agent.models import Position


@dataclass
class OrderResult:
    filled_qty: int
    avg_price: float
    message: str


class Broker(ABC):
    @abstractmethod
    def buy(self, symbol: str, qty: int, price: float) -> OrderResult:
        raise NotImplementedError

    @abstractmethod
    def sell(self, symbol: str, qty: int, price: float) -> OrderResult:
        raise NotImplementedError


class PaperBroker(Broker):
    """In-memory broker implementation for dry-run or integration testing."""

    def __init__(self):
        self.positions: dict[str, Position] = {}

    def buy(self, symbol: str, qty: int, price: float) -> OrderResult:
        if qty <= 0:
            return OrderResult(0, 0.0, "Rejected: qty must be > 0")
        return OrderResult(qty, price, "Filled")

    def sell(self, symbol: str, qty: int, price: float) -> OrderResult:
        if qty <= 0:
            return OrderResult(0, 0.0, "Rejected: qty must be > 0")
        return OrderResult(qty, price, "Filled")
