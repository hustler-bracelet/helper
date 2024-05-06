from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.widgets import NumberInput
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
        NumberInput(on_success=get_base_amount_for_new_asset),
        state=states.AddFinanceAsset.BASE_AMOUNT
    ),
    Window(
        Const(
            '➕ <b>Добавление актива</b>\n'
            '\n'
            'Какой годовой процент? Если ты хочешь добавлять прибыль вручную, напишите 0'
        ),
        NumberInput(on_success=get_interest_rate_for_new_asset),
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
