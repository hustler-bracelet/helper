
from pydantic import BaseModel


class TelegramUserID(BaseModel):
    telegram_id: int


class User(TelegramUserID):
    telegram_name: str

    class Config:
        orm_mode = True
