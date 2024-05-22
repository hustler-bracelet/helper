# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class ActivityTask(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    niche_id: int = Field(foreign_key='niche.id')
    name: str
    description: str
    points: int
    added_on: datetime
    deadline: datetime
