from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states


async def get_name_for_new_event(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['asset_name'] = data
    await dialog_manager.next()


add_asset_dialog = Dialog(
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Введите название актива:'
        ),
        TextInput(
            id='get_name_for_new_asset',
            on_success=get_name_for_new_event
        ),
        state=states.AddFinanceAsset.MAIN
    ),
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Какой годовой процент? Если вы хотите добавлять прибыль вручную, напишите 0'
        ),
        TextInput(
            id='get_percent_of_new_asset',
            on_success=...,
            filter=...  # Фильтр имеет возможность обрабатывать данные. Выхлоп фильтра будет в data функции on_success.
            # Если фильтр выбросит ValueError - вызовется on_error.
            # Пример фильтра найди где-то в коде по ключевому слову "filter="
        ),
        state=states.AddFinanceAsset.PERCENT
    )
)
