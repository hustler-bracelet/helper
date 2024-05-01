import operator

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.common.items import ItemsGetterVariant
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Back
from aiogram_dialog.widgets.kbd.select import OnItemClick, Select
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def get_name_for_new_asset(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['asset_name'] = data
    await dialog_manager.next()


async def get_interest_rate_for_new_asset(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['interest_rate'] = data

    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']
    await finance_manager.add_asset(
        name=dialog_manager.dialog_data['asset_name'],
        base_amount=dialog_manager.dialog_data['base_amount'],
        interest_rate=dialog_manager.dialog_data['interest_rate']
    )

    await dialog_manager.next()


async def get_base_amount_for_new_asset(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['base_amount'] = data
    await dialog_manager.next()


add_asset_dialog = Dialog(
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Введите название актива:'
        ),
        Cancel(Const('⬅️ Назад')),
        TextInput(
            id='get_name_for_new_asset',
            on_success=get_name_for_new_asset
        ),
        state=states.AddFinanceAsset.MAIN
    ),
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Введите сумму депозита:'
        ),
        TextInput(
            id='get_base_amount_for_new_asset',
            on_success=get_base_amount_for_new_asset
        ),
        state=states.AddFinanceAsset.BASE_AMOUNT
    ),
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Какой годовой процент? Если вы хотите добавлять прибыль вручную, напишите 0'
        ),
        TextInput(
            id='get_percent_of_new_asset',
            on_success=get_interest_rate_for_new_asset
            # filter=...  # Фильтр имеет возможность обрабатывать данные. Выхлоп фильтра будет в data функции on_success.
            # Если фильтр выбросит ValueError - вызовется on_error.
            # Пример фильтра найди где-то в коде по ключевому слову "filter="
        ),
        state=states.AddFinanceAsset.INTEREST_RATE
    ),
    Window(
        Format(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Актив {dialog_data[asset_name]} под {dialog_data[interest_rate]}% добавлен.'
        ),
        Cancel(Const('👌 Ок')),
        state=states.AddFinanceAsset.FINAL
    )
)
