import datetime

import config

from aiogram import html
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.about import about_aiogram_dialog_button
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils.lang_utils import plural_form, format_number
from hustler_bracelet.managers import FinanceManager


async def bot_statistics_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    bot_drop_date = datetime.date(2024, 5, 1)

    today = datetime.date.today()

    days_delta = today.day - bot_drop_date.day
    months_delta = today.month - bot_drop_date.month
    years_delta = today.year - bot_drop_date.year

    texted_bot_work_time = plural_form(days_delta or 1, ['день', 'дня', 'дней'])
    if months_delta:
        texted_bot_work_time = plural_form(months_delta or 1, ['месяц', 'месяца', 'месяцев'])
    if years_delta:
        texted_bot_work_time = plural_form(years_delta or 1, ['год', 'года', 'лет'])

    return {
        'users_amount': await finance_manager.get_users_amount(),
        'bot_work_time': texted_bot_work_time
    }


about_bot_dialog = Dialog(
    Window(
        Jinja(
            '\n'
            '💪 <b>Бот HUSTLER HELPER!</b>\n'
            '\n'
            '📊 Уже <b>{{ bot_work_time }}</b> <b>{{ users_amount|plural(["пользователь", "пользователя", "пользователей"]) }}</b> делают систему из своих движений. А что насчёт тебя?\n'
            '\n'
            '👨‍💻 <b>Бот сделан:</b>\n'
            '@d_nsdkin & @farel106\n'
            '\n'
            '⚙️ <b>Версия бота:</b>\n'
            f'hustler_bracelet {config.VERSION} от {config.UPDATE_TIME}\n'
            '\n'
            f'Бот основан на {html.link("aiogram3", link="https://github.com/aiogram/aiogram")} (by RootJunior and the aiogram team) '
            f'и {html.link("aiogram_dialog", link="https://github.com/Tishka17/aiogram_dialog")} (by Tishka17).'
        ),
        about_aiogram_dialog_button(),
        Cancel(Const('👌 Ок')),
        state=states.AboutBot.MAIN,
        getter=bot_statistics_getter
    )
)
