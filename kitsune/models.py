from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class Trade(BaseModel):
    exchange: str
    symbol: str
    price: Decimal
    amount: Decimal
    side: Literal["buy", "sell"]
    traded_at: datetime


class OrderbookSnapshot(BaseModel):
    exchange: str
    symbol: str
    bids: list[list[Decimal]]
    asks: list[list[Decimal]]
    snapshot_at: datetime
