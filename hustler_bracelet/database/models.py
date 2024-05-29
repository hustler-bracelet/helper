
from sqlalchemy import ForeignKey, Enum, BigInteger, DateTime, Text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import func
from datetime import datetime, date

from hustler_bracelet.enums import (
    CompletionStatus, 
    PayoutReason, 
    PaymentReason,
)


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    telegram_name: Mapped[str] = mapped_column()

    current_balance: Mapped[float] = mapped_column(default=0.0)
    referred_by: Mapped[int | None] = mapped_column(ForeignKey('user.telegram_id'), nullable=True)
    is_participating_in_activity: Mapped[bool] = mapped_column(default=False)
    selected_niche_id: Mapped[int | None] = mapped_column(ForeignKey('niche.id'))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ActivityTaskCompletion(BaseModel):
    __tablename__ = 'activity_task_completion'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger())
    activity_task_id: Mapped[int] = mapped_column(ForeignKey('activity_task.id'))
    proof_id: Mapped[int] = mapped_column(ForeignKey('task_completion_proof.id'))
    status: Mapped[CompletionStatus] = mapped_column(Enum(CompletionStatus), default=CompletionStatus.PENDING, server_default='PENDING')
    sent_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    checked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    points: Mapped[int]


class ActivityTask(BaseModel):
    __tablename__ = 'activity_task'

    id: Mapped[int] = mapped_column(primary_key=True)
    niche_id: Mapped[int] = mapped_column(ForeignKey('niche.id'))
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    points: Mapped[int]
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Activity(BaseModel):
    __tablename__ = 'activity'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    emoji: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    fund: Mapped[int]
    total_places: Mapped[int]
    occupied_places: Mapped[int]
    started_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_running: Mapped[bool]


class Asset(BaseModel):
    __tablename__ = 'asset'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    name: Mapped[str] = mapped_column(Text)
    interest_rate: Mapped[float] = mapped_column(default=0.0)
    base_amount: Mapped[float]
    current_amount: Mapped[float]


class Category(BaseModel):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)


class FinanceTransaction(BaseModel):
    __tablename__ = 'financetransaction'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[str] = mapped_column(Text)
    category: Mapped[int] = mapped_column(ForeignKey('category.id'))
    value: Mapped[float]
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction_date: Mapped[date]


class InvestmentTransaction(BaseModel):
    __tablename__ = 'investmenttransaction'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    type: Mapped[str | None] = mapped_column(Text, default=None, nullable=True)
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    asset_id: Mapped[int] = mapped_column(ForeignKey('asset.id'))
    value: Mapped[float]


class Niche(BaseModel):
    __tablename__ = 'niche'

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'))
    name: Mapped[str] = mapped_column(Text)
    emoji: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class Payment(BaseModel):
    __tablename__ = 'user_payment'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    yookassa_payment_info: Mapped[str | None]
    payment_reason: Mapped[PaymentReason] = mapped_column(Enum(PaymentReason))
    amount_rub: Mapped[float]
    paid_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payout(BaseModel):
    __tablename__ = 'user_payout'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    reason: Mapped[PayoutReason] = mapped_column(Enum(PayoutReason))
    amount_rub: Mapped[float]
    paid_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TaskCompletionProof(BaseModel):
    __tablename__ = 'task_completion_proof'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    activity_task_id: Mapped[int] = mapped_column(ForeignKey('activity_task.id'))
    message_text: Mapped[str] = mapped_column(Text)
    media: Mapped[str] = mapped_column(Text)
    sent_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Task(BaseModel):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    name: Mapped[str] = mapped_column(Text)
    added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    planned_complete_date: Mapped[date]
    is_completed: Mapped[bool] = mapped_column(default=False)
