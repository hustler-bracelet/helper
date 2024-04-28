# -*- coding: utf-8 -*-

from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import FinanceTransactionType


class FinanceTransaction(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    type: FinanceTransactionType
    category: int = Field(foreign_key='category.id')
    value: float
    added_on: datetime
    transaction_date: date
