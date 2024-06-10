import asyncio
import logging

import aiogram_dialog
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from aiogram_album.count_check_middleware import CountCheckAlbumMiddleware
from aiogram_dialog import DialogManager, setup_dialogs, ShowMode, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent
from aiogram_dialog.widgets.text import setup_jinja

import config
from hustler_bracelet.bot.dialogs.activity.choose_hiche import choose_niche_dialog
from hustler_bracelet.bot.dialogs.activity.complete_task import complete_task_dialog
from hustler_bracelet.bot.dialogs.activity.list import activities_list_dialog
from hustler_bracelet.bot.dialogs.activity.quit import activity_quit_dialog
from hustler_bracelet.bot.dialogs.activity.task import activity_task_dialog
from hustler_bracelet.bot.dialogs.finance import finance_menu_dialog
from hustler_bracelet.bot.dialogs.finance.add_event import add_finance_event_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management import finance_categories_management_menu_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management.add_category import add_finance_category_dialog
from hustler_bracelet.bot.dialogs.finance.categories_management.delete_category import delete_finance_category_dialog
from hustler_bracelet.bot.dialogs.finance.investments import investments_main_menu_dialog
from hustler_bracelet.bot.dialogs.finance.investments.add_asset import add_asset_dialog
from hustler_bracelet.bot.dialogs.finance.investments.add_profit import add_profit_dialog
from hustler_bracelet.bot.dialogs.finance.investments.change_interest_rate import change_interest_rate_dialog
from hustler_bracelet.bot.dialogs.finance.investments.delete_asset import delete_assets_dialog
from hustler_bracelet.bot.dialogs.finance.investments.rename_asset import rename_asset_dialog
from hustler_bracelet.bot.dialogs.finance.list_events import list_finance_events_menu_dialog
from hustler_bracelet.bot.dialogs.main import main_dialog
from hustler_bracelet.bot.dialogs.onboarding import onboarding_dialog
from hustler_bracelet.bot.dialogs.planning import planning_main_menu_dialog
from hustler_bracelet.bot.dialogs.planning.add_task import add_task_dialog
from hustler_bracelet.bot.dialogs.planning.complete_some_tasks import complete_some_tasks_dialog
from hustler_bracelet.bot.dialogs.settings import settings_main_menu_dialog
from hustler_bracelet.bot.dialogs.settings.about_bot import about_bot_dialog
from hustler_bracelet.bot.dialogs.settings.erase_all_data_about_me import erase_all_data_about_me_dialog
from hustler_bracelet.bot.dialogs.settings.fix_balance import fix_balance_menu_dialog
from hustler_bracelet.bot.dialogs.sport import sport_main_menu_dialog
from hustler_bracelet.bot.dialogs.activity import activity_dialog
from hustler_bracelet.bot.filters import SubChecker
from hustler_bracelet.bot.middlewares import database_middleware
from hustler_bracelet.bot.utils.lang_utils import get_jinja_filters
from hustler_bracelet.bot.dialogs.activity.admin import admin_router
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


# TODO: Сделать хендлинг необработанных ошибок


dialog_router = Router()

dialog_router.include_routers(
    fix_balance_menu_dialog,
    list_finance_events_menu_dialog,
    investments_main_menu_dialog,
    onboarding_dialog,
    erase_all_data_about_me_dialog,
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
    add_asset_dialog,
    delete_assets_dialog,
    add_profit_dialog,
    rename_asset_dialog,
    change_interest_rate_dialog,
    activity_dialog,
    activity_quit_dialog,
    activity_task_dialog,
    complete_task_dialog,
    choose_niche_dialog,
    activities_list_dialog
)


def setup_dp():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.register(start, F.text == "/start")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    dp.include_router(admin_router)

    dp.message.middleware.register(database_middleware)
    dp.callback_query.middleware.register(database_middleware)
    dp.errors.middleware.register(database_middleware)

    dp.message.filter(SubChecker())

    dp.include_router(dialog_router)

    setup_dialogs(dp)

    return dp


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.TG_BOT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    dp = setup_dp()

    CountCheckAlbumMiddleware(router=dp)

    aiogram_dialog.widgets.text.jinja.default_env = setup_jinja(dp, filters=get_jinja_filters())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
