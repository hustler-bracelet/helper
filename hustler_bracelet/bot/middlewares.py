from typing import Callable, Any, Awaitable

from aiogram import types, BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from sqlmodel.ext.asyncio.session import AsyncSession

from config import BRACELET_CHANNEL_ID
from hustler_bracelet.database.engine import DATABASE_ENGINE
from hustler_bracelet.managers import UserManager, FinanceManager


async def database_middleware(
        handler: Callable[[types.Update | types.ErrorEvent, dict[str, Any]], Awaitable[Any]],
        event: types.Update | types.ErrorEvent,
        data: dict[str, Any]
) -> Any:
    raw_event = event
    if isinstance(event, types.ErrorEvent):
        event, exception = event.update, event.exception
        event = event.message or event.callback_query
        if event is None:
            raise exception

    data['user_manager'] = user_manager = UserManager(event.from_user.id, AsyncSession(DATABASE_ENGINE))
    data['finance_manager'] = FinanceManager(user_manager)

    async with user_manager:
        data['user_created'] = await user_manager.create_user_if_not_exists(event.from_user.first_name)
        return await handler(raw_event, data)
