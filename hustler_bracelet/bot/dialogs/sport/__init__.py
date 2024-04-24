from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states

sport_main_menu_dialog = Dialog(
    Window(
        Const('Пока что в разработке...'),
        Cancel(Const('Ok')),
        state=states.Sport.MAIN
    )
)
