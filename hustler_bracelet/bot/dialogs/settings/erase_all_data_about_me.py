from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Cancel
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def on_sure_erase_all_data_about_me_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']
    await finance_manager.erase_all_data_about_user(callback.from_user.id)
    await manager.next()


erase_all_data_about_me_dialog = Dialog(
    Window(
        Const(
            '🗑 <b>Удаление информации</b>\n'
            '\n'
            'Ты уверен, что хочешь удалить <b>всю</b> информацию о себе из бота? '
            'Это действие нельзя будет отменить, будет удалена абсолютно вся информация'
        ),
        Row(
            Button(
                Const('✅ УДАЛИТЬ'),
                id='sure_erase_all_data_about_me',
                on_click=on_sure_erase_all_data_about_me_click
            ),
            Cancel(Const('❌ Нет, отмена'))
        ),
        state=states.EraseAllDataAboutUser.MAIN
    ),
    Window(
        Const(
            '🗑 <b>Удаление информации</b>\n'
            '\n'
            'Прощай. Это было хорошее время.'
        ),
        Cancel(Const('👋 Пока')),
        state=states.EraseAllDataAboutUser.FINAL
    )
)
