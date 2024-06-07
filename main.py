from __future__ import annotations

import asyncio
import datetime

from hustler_bracelet import bot
from hustler_bracelet.bot.utils.lang_utils import represent_datetime


# from hustler_bracelet.database.engine import create_all_tables


async def main():
    # await create_all_tables()
    await bot.main()


asyncio.run(main())
