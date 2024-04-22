# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import FinanceTransactionType


class Category(SQLModel, AsyncAttrs, table=True):
    uuid: str = Field(primary_key=True)
    telegram_id: int = Field(foreign_key="user.telegram_id")
    name: str
    type: FinanceTransactionType
