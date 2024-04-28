import asyncio
import logging
from typing import Callable, Any, Awaitable

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove, Update
from aiogram_dialog import DialogManager, setup_dialogs, ShowMode, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent
from sqlmodel.ext.asyncio.session import AsyncSession

import config
from hustler_bracelet.bot.dialogs.finance import finance_menu_dialog
from hustler_bracelet.bot.dialogs.finance.add_event import add_finance_event_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management import finance_categories_management_menu_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management.add_category import add_finance_category_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management.delete_category import delete_finance_category_dialog
from hustler_bracelet.bot.dialogs.main import main_dialog
from hustler_bracelet.bot.dialogs.onboarding import onboarding_dialog
from hustler_bracelet.bot.dialogs.settings import settings_main_menu_dialog
from hustler_bracelet.bot.dialogs.settings.about_bot import about_bot_dialog
from hustler_bracelet.bot.dialogs.sport import sport_main_menu_dialog
from hustler_bracelet.bot.dialogs.planning import planning_main_menu_dialog
from hustler_bracelet.bot.dialogs.planning.add_task import add_task_dialog
from hustler_bracelet.bot.dialogs.planning.complete_some_tasks import complete_some_tasks_dialog
from hustler_bracelet.database.engine import DATABASE_ENGINE
from hustler_bracelet.managers.finance_manager import FinanceManager
from hustler_bracelet.managers.user_manager import UserManager
from .dialogs import states


async def start(message: Message, dialog_manager: DialogManager):
    if dialog_manager.middleware_data['user_created']:
        await dialog_manager.start(states.OnBoarding.MAIN)
        return

    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот был перезапущен из-за технических работ.\n"
            "Переходим в главное меню.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            "Бот был перезапущен из-за технических работ.\n"
            "Переходим в главное меню.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await dialog_manager.start(
        states.Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


dialog_router = Router()

dialog_router.include_routers(
    onboarding_dialog,
    main_dialog,
    sport_main_menu_dialog,
    delete_finance_category_dialog,
    planning_main_menu_dialog,
    add_task_dialog,
    complete_some_tasks_dialog,
    settings_main_menu_dialog,
    about_bot_dialog,
    finance_menu_dialog,
    finance_categories_management_menu_dialog,
    add_finance_event_dialog,
    add_finance_category_dialog,
)


def setup_dp():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.register(start, F.text == "/start")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    return dp


async def database_middleware(
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
) -> Any:
    familiar_event: types.Message | types.CallbackQuery = event.message or event.callback_query

    if familiar_event:
        data['user_manager'] = user_manager = UserManager(familiar_event.from_user.id, AsyncSession(DATABASE_ENGINE))
        data['finance_manager'] = FinanceManager(user_manager)

        async with user_manager:
            data['user_created'] = await user_manager.create_user_if_not_exists(familiar_event.from_user.first_name)
            return await handler(event, data)
    else:
        print(f'Some strange event: {event}')
        return await handler(event, data)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.TG_BOT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    dp = setup_dp()

    dp.update.outer_middleware.register(database_middleware)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
