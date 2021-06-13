from enum import Enum
from pydantic import BaseModel


class ExchangeEnum(str, Enum):
    coinbasepro = "coinbasepro"
    gemini = "gemini"


class Product(BaseModel):
    symbol: str


class SideEnum(str, Enum):
    buy = "buy"
    sell = "sell"


class Stratagies(str, Enum):
    GRID = "GRID"
    DCA = "DCA"


class Trade(BaseModel):
    side: SideEnum
    count: int
    price: float
    diff: float
    size: float
    profit: float
    symbol: str
    strategy: Stratagies
