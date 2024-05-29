# -*- coding: utf-8 -*-

import config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import URL
from sqlmodel import create_engine, SQLModel

DATABASE_ENGINE = AsyncEngine(
    create_engine(
        url=URL(
            drivername='postgresql+asyncpg',
            username=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            query={}
        )
    )
)
# DATABASE_ENGINE = AsyncEngine(create_engine('sqlite+aiosqlite:///hustler_bracelet.sqlite'))


async def create_all_tables() -> None:
    async with DATABASE_ENGINE.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # return await conn.run_sync(SQLModel.metadata.create_all)
        pass
