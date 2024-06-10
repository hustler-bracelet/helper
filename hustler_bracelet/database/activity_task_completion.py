# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field

from hustler_bracelet.enums import ProofCompletionStatus


class ActivityTaskCompletion(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(sa_column=Column(BigInteger()))
    activity_task_id: int = Field(foreign_key='activitytask.id')
    proof_id: int = Field(foreign_key='taskcompletionproof.id')
    status: ProofCompletionStatus
    sent_on: datetime
    checked_on: datetime
    points: int
