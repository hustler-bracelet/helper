# -*- coding: utf-8 -*-

from sqlmodel import SQLModel, Field
from .finance_transaction_type import FinanceTransactionType
from datetime import datetime, date


class FinanceTransaction(SQLModel, table=True):
    uuid: str = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    type: FinanceTransactionType
    category: str = Field(foreign_key='category.name')
    value: float
    added_on: datetime
    transaction_date: date
