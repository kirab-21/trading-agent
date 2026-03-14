from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from trading_agent.models import Candle


DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y %H:%M:%S",
]


def parse_datetime(value: str) -> datetime:
    for fmt in DATETIME_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported datetime format: {value}")


def load_candles_from_csv(path: str | Path) -> List[Candle]:
    path = Path(path)
    candles: List[Candle] = []

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required_cols = {"datetime", "open", "high", "low", "close", "volume"}
        if reader.fieldnames is None or not required_cols.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must include columns: datetime,open,high,low,close,volume")

        for row in reader:
            candles.append(
                Candle(
                    timestamp=parse_datetime(row["datetime"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )
            )

    return candles
