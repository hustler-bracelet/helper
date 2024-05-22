# -*- coding: utf-8 -*-

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class User(SQLModel, AsyncAttrs, table=True):
    telegram_id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False)
    )
    telegram_name: str
    current_balance: float = Field(default=0.0)
    referred_by: int = Field(sa_column=Column(BigInteger()))
    is_participating_in_activity: bool = Field(default=False)
    selected_niche_id: int | None
