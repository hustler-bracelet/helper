from typing import Callable, Any, Awaitable

from aiogram import types, BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from sqlmodel.ext.asyncio.session import AsyncSession

from config import BRACELET_CHANNEL_ID
from hustler_bracelet.database.engine import DATABASE_ENGINE
from hustler_bracelet.managers import UserManager, FinanceManager


async def database_middleware(
        handler: Callable[[types.Update, dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: dict[str, Any]
) -> Any:
    data['user_manager'] = user_manager = UserManager(event.from_user.id, AsyncSession(DATABASE_ENGINE))
    data['finance_manager'] = FinanceManager(user_manager)

    async with user_manager:
        data['user_created'] = await user_manager.create_user_if_not_exists(event.from_user.first_name)
        return await handler(event, data)
