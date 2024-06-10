
from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    symbol: str
    code: str


class CurrencyRUB(Currency):
    name: str = 'Russian ruble'
    symbol: str = '₽'
    code: str = 'RUB'
