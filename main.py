from __future__ import annotations

import asyncio

from hustler_bracelet import bot
# from hustler_bracelet.database.engine import create_all_tables


async def main():
    # await create_all_tables()
    await bot.main()


asyncio.run(main())
