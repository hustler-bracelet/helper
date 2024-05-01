import datetime
import operator
from datetime import date
from typing import Any

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.common.items import ItemsGetterVariant
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel, Calendar, ManagedCalendar, CalendarConfig, Back, ScrollingGroup
from aiogram_dialog.widgets.kbd.select import OnItemClick, Select
from aiogram_dialog.widgets.text import Const, Format, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.widgets import Today
from hustler_bracelet.managers import FinanceManager


async def on_asset_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: int
):
    manager.dialog_data['asset_id'] = item_id

    await manager.next()


async def on_profit_entered(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: float
):
    dialog_manager.dialog_data['profit'] = float(data)

    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    await finance_manager.record_asset_profit(
        asset=int(dialog_manager.dialog_data['asset_id']),
        profit=data
    )
    await dialog_manager.done()


# async def on_date_clicked(
#         callback: ChatEvent,
#         widget: ManagedCalendar | None,
#         manager: DialogManager,
#         selected_date: date
# ):
#     finance_manager: FinanceManager = manager.middleware_data['finance_manager']
#
#     manager.dialog_data['date'] = selected_date
#
#     await finance_manager.add_task(
#         name=manager.dialog_data['name'],
#         planned_complete_date=selected_date
#     )
#
#     await manager.next()

# скоро понадобится


def get_choose_asset_kb(on_choose_asset_click: OnItemClick, items: ItemsGetterVariant = 'assets'):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='slct_categories',
            item_id_getter=operator.itemgetter(1),
            items=items,
            on_click=on_choose_asset_click
        ),
        id="scrl_assets",
        width=1,
        height=6,
        hide_on_single_page=True
    )


async def asset_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']
    assets = await finance_manager.get_all_assets()

    return {
        'assets': [(asset.name, asset.id) for asset in assets]
    }


add_profit_dialog = Dialog(
    Window(
        Const(
            '🤑 <b>Добавление прибыли</b>\n'
            '\n'
            'По какому активу тебе пришла прибыль?'
        ),
        get_choose_asset_kb(on_asset_selected),
        Cancel(Const('❌ Отмена')),
        state=states.AddInvestmentProfit.MAIN
    ),
    Window(
        Const(
            '🤑 <b>Добавление прибыли</b>\n'
            '\n'
            'Сколько ты заработал?'
        ),
        TextInput(
            id='asset_profit_amount',
            on_success=on_profit_entered
        ),
        Back(Const('⬅️ Назад')),
        state=states.AddInvestmentProfit.PROFIT
    ),
    getter=asset_getter
)
