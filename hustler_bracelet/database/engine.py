# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine, SQLModel

DATABASE_ENGINE = AsyncEngine(create_engine('sqlite+aiosqlite:///hustler_bracelet.sqlite', echo=True, future=True))


async def create_all_tables() -> None:
    async with DATABASE_ENGINE.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        return await conn.run_sync(SQLModel.metadata.create_all)
