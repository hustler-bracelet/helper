# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class InvestmentTransaction(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    added_on: datetime
    asset_id: int = Field(foreign_key='asset.id')
    value: float
