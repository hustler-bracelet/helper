import config

from aiogram import html
from aiogram_dialog import Dialog, Window
from aiogram_dialog.about import about_aiogram_dialog_button
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states

about_bot_dialog = Dialog(
    Window(
        Const(
            '\n'
            '💪 <b>Бот HUSTLER HELPER!</b>\n'
            '\n'
            '📊 Уже <b>1 месяц и 2 дня</b> <b>340</b> пользователей делают систему из своих движений. А что насчёт тебя?\n'
            '\n'
            '👨‍💻 <b>Бот сделан:</b>\n'
            '@d_nsdkin & @farel106'
            '\n'
            '⚙️ <b>Версия бота:</b>\n'
            f'hustler_bracelet {config.VERSION} от {config.UPDATE_TIME}\n'
            '\n'
            f'Бот основан на {html.link("aiogram3", link="https://github.com/aiogram/aiogram")} (by RootJunior and the aiogram team) '
            f'и {html.link("aiogram_dialog", link="https://github.com/Tishka17/aiogram_dialog")} (by Tishka17).'
        ),
        about_aiogram_dialog_button(),
        Cancel(Const('Ok')),
        state=states.AboutBot.MAIN
    )
)
