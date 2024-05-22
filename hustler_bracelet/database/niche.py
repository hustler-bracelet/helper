# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class Niche(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    activity_id: int = Field(foreign_key='activity.id')
    name: str
    emoji: str
    description: str
