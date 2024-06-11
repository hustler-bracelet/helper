
from pydantic import BaseModel

from .user import User
from .currency import CurrencyRUB


class EarnData(BaseModel):
    currency: CurrencyRUB = CurrencyRUB()
    sum: float


class LeaderBoardItem(BaseModel):
    user: User
    earn: EarnData
    points: int
    position: int
