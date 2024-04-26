# -*- coding: utf-8 -*-
from sqlmodel.ext.asyncio.session import AsyncSession

from hustler_bracelet.database.engine import DATABASE_ENGINE


class PlanningManager:
    def __init__(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
        self._session = AsyncSession(DATABASE_ENGINE)
