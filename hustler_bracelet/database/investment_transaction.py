# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import FinanceTransactionType


class InvestmentTransaction(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(sa_column=Column(BigInteger()))
    type: str | None = Field(default=None)
    added_on: datetime
    asset_id: int = Field(foreign_key='asset.id')
    value: float
