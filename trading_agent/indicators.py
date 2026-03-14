from __future__ import annotations

from typing import List


def ema(values: List[float], period: int) -> List[float]:
    if period <= 0:
        raise ValueError("period must be > 0")
    if not values:
        return []

    multiplier = 2 / (period + 1)
    output = [values[0]]
    for value in values[1:]:
        output.append((value - output[-1]) * multiplier + output[-1])
    return output


def rsi(closes: List[float], period: int = 14) -> List[float]:
    if period <= 0:
        raise ValueError("period must be > 0")
    if len(closes) < 2:
        return [50.0 for _ in closes]

    gains = [0.0]
    losses = [0.0]
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))

    avg_gain = 0.0
    avg_loss = 0.0
    output: List[float] = []

    for i in range(len(closes)):
        if i < period:
            output.append(50.0)
            avg_gain += gains[i]
            avg_loss += losses[i]
            continue

        if i == period:
            avg_gain = sum(gains[1 : period + 1]) / period
            avg_loss = sum(losses[1 : period + 1]) / period
        else:
            avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
            avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

        if avg_loss == 0:
            output.append(100.0)
        else:
            rs = avg_gain / avg_loss
            output.append(100 - (100 / (1 + rs)))

    return output


def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
    if period <= 0:
        raise ValueError("period must be > 0")
    if not highs or not lows or not closes:
        return []
    if not (len(highs) == len(lows) == len(closes)):
        raise ValueError("highs, lows, closes must have same length")

    true_ranges = [highs[0] - lows[0]]
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        true_ranges.append(tr)

    return ema(true_ranges, period)
