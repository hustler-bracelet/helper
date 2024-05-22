import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, NumberedPager, Back, Cancel
from aiogram_dialog.widgets.text import Format, Const, List, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.finance.widgets import get_choose_category_type_kb
from hustler_bracelet.bot.utils.lang_utils import finance_event_words_getter
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers import FinanceManager


async def on_events_type_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
):
    manager.dialog_data['event_type'] = FinanceTransactionType(item_id.upper())
    await manager.next()


async def finance_events_getter(dialog_manager: DialogManager, finance_manager: FinanceManager, **kwargs):
    events = await finance_manager.get_all_events(dialog_manager.dialog_data['event_type'])
    return {
        'finance_events': [
            (
                await event.awaitable_attrs.transaction_date,
                await event.awaitable_attrs.value,
                await (await finance_manager.get_category_by_id(await event.awaitable_attrs.category)).awaitable_attrs.name,
            ) for event in events
        ]
    }


list_finance_events_menu_dialog = Dialog(
    Window(
        Const(
            '🕔 <b>История транзакций</b>\n'
            '\n'
            'Транзакции какого типа тебя интересуют?'
        ),
        get_choose_category_type_kb(on_events_type_selected),
        Cancel(Const('❌ Отмена')),
        state=states.FinanceEventsListMenu.MAIN
    ),
    Window(
        Format('🕔 <b>История {finance_event_name}ов:</b>'),
        List(
            Jinja('{{ item[0]|date }} {{ data.finance_event_name }} {{ item[1]|money }} в категории {{ item[2] }}'),
            items='finance_events',
            id='lst_scrl_finance_events',
            page_size=10,
        ),
        NumberedPager(
            scroll='lst_scrl_finance_events',
        ),
        Cancel(Const('👌 Ок')),
        state=states.FinanceEventsListMenu.LIST,
        getter=(finance_events_getter, finance_event_words_getter)
    )
)
