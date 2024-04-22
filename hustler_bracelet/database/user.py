# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class User(SQLModel, AsyncAttrs, table=True):
    telegram_id: int = Field(primary_key=True)
    telegram_name: str
    current_balance: float = Field(default=0.0)
