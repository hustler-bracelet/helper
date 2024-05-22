# -*- coding: utf-8 -*-

from datetime import datetime, date

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import FinanceTransactionType


class FinanceTransaction(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(sa_column=Column(BigInteger()))
    type: str
    category: int = Field(foreign_key='category.id')
    value: float
    added_on: datetime
    transaction_date: date
