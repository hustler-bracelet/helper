# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class Asset(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    added_on: datetime
    name: str
    interest_rate: float = Field(default=0.0)
    base_amount: float
    current_amount: float
