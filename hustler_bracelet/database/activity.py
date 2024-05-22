# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class Activity(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    emoji: str
    description: str
    fund: int
    total_places: int
    occupied_places: int
    started_on: datetime
    deadline: datetime
    is_running: bool
