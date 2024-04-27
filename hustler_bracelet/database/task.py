from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field


class Task(SQLModel, AsyncAttrs, table=True):
    id: int | None = Field(primary_key=True)
    telegram_id: int = Field(foreign_key='user.telegram_id')
    name: str
    added_on: datetime
    planned_complete_date: date
    is_completed: bool = Field(default=False)
