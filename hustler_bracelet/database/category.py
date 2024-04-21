# -*- coding: utf-8 -*-

from .finance_transaction_type import FinanceTransactionType
from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    uuid: str = Field(primary_key=True)
    telegram_id: int = Field(foreign_key="user.telegram_id")
    name: str
    type: FinanceTransactionType
