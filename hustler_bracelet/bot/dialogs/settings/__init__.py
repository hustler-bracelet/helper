from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states

settings_main_menu_dialog = Dialog(
    Window(
        Const(
            '⚙️ <b>Настройки</b>\n'
            '\n'
            '<b>Валюта:</b> рубли'
        ),
        Start(
            Const('Изменить: Валюта'),
            id='change_currency_setting',
            state=states.ChangeCurrencySetting.MAIN
        ),
        Start(
            Const('ℹ️ О боте'),
            id='about_bot',
            state=states.AboutBot.MAIN
        ),
        Start(
            Const('🗑 Стереть все данные обо мне'),
            id='erase_all_data_about_user',
            state=states.EraseAllDataAboutUser.MAIN
        ),
        Cancel(Const('❌ Отмена')),
        state=states.SettingsMainMenu.MAIN
    )
)
