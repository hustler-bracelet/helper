from __future__ import annotations

import asyncio

from hustler_bracelet import bot
from hustler_bracelet.controllers.category import Category

# from hustler_bracelet.database import UserTable, CategoryTable, EventTable
#
# user = UserTable.get_by_id(0)
# category1 = CategoryTable.get_by_id(0)
# category2 = CategoryTable.get_by_id(1)
# event1 = EventTable.get_by_id(0)
# event2 = EventTable.get_by_id(1)
#
# query = (
#     category1.events.where(EventTable.id == 1)
# )
#
# for event in query:
#     print(event.name)

asyncio.run(bot.main())
