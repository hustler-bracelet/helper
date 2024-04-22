# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field
from datetime import datetime, date

from hustler_bracelet.enums import FinanceTransactionType


class FinanceTransaction(SQLModel, AsyncAttrs, table=True):
    uuid: str = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    type: FinanceTransactionType
    category: str = Field(foreign_key='category.uuid')
    value: float
    added_on: datetime
    transaction_date: date
