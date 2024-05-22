# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import PaymentReason


class Payment(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(sa_column=Column(BigInteger()))
    yookassa_payment_info: str | None
    payment_reason: PaymentReason
    amount_rub: float
    paid_on: datetime
