import datetime
import re
from datetime import date

from aiogram import types, Dispatcher
from aiogram.types import ForceReply
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Calendar, ManagedCalendar, Button, ScrollingGroup, Back, Start, CalendarConfig
)
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.bot_dialogs import states
from hustler_bracelet.bot.bot_dialogs.common import MAIN_MENU_BUTTON
from hustler_bracelet.bot.callbacks import CategoryForNewEventCallback
from hustler_bracelet.bot.lang_utils import get_finance_event_type_verb, finance_event_words_getter
from hustler_bracelet.enums import FinanceEventType


async def on_date_clicked(
        callback: ChatEvent,
        widget: ManagedCalendar | None,
        manager: DialogManager,
        selected_date: date,
):
    await callback.answer(str(selected_date))
    manager.dialog_data['event_date'] = selected_date
    await manager.next()


async def on_today_clicked(
        callback: ChatEvent,
        button: Button,
        manager: DialogManager,
):
    return await on_date_clicked(
        callback=callback,
        widget=None,
        manager=manager,
        selected_date=date.today()
    )


async def on_add_category_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.start(
        state=states.AddFinanceCategory.ENTER_NAME,  # Скипаем первый этап, т.к. ответ на первый вопрос (тип категории) уже известен
        data={'cat_type': manager.start_data['event_type']}
    )


async def on_choose_category_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    manager.dialog_data['category_id'] = CategoryForNewEventCallback.unpack(value=callback.data).category_id
    # event_date = manager.dialog_data['event_date']

    await manager.next()


async def get_amount_for_new_event(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: float
):
    dialog_manager.dialog_data['value'] = data
    await dialog_manager.next()


async def process_incorrect_amount_for_new_event(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError,
):
    await message.answer('\n'.join([error.args, 'Попробуй ещё раз']))


def validate_amount_for_new_event(text: str):
    amount = text.lower()

    replace_mapping = {
        'к': 'k',
        'r': 'k',
        'л': 'k',

        ' ': '',

        ',': '.',
        'б': '.',
        'ю': '.',
        '?': '.',
    }
    for old, new in replace_mapping.items():
        amount = amount.replace(old, new)

    if 'k' in amount.rstrip('k'):
        raise ValueError('Неправильный формат числа')

    try:
        amount = float(amount.rstrip('k')) * (1000 ** amount.count('k'))
    except ValueError:
        raise ValueError('Неправильный формат числа')

    return amount


# async def data_getter_for_final_window(dialog_manager: DialogManager, **kwargs):
#     return {**dialog_manager.dialog_data, **dialog_manager.start_data}


add_event_dialog = Dialog(
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'Выбери категорию {finance_event_name}а или создай новую:'
        ),
        ScrollingGroup(
            Button(text=Const('Банки'), id=CategoryForNewEventCallback(category_id=0).pack(), on_click=on_choose_category_click),
            Button(text=Const('Хуянки'), id=CategoryForNewEventCallback(category_id=1).pack(), on_click=on_choose_category_click),
            id="fin_category",
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Button(text=Const('➕ Создать новую категорию'), id='add_fin_category', on_click=on_add_category_click),
        MAIN_MENU_BUTTON,
        state=states.AddFinanceEvent.MAIN,
    ),
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'Введи сумму, которую ты {finance_event_verb} (в рублях):'
        ),
        TextInput(
            id='amount_of_new_event',
            on_success=get_amount_for_new_event,
            on_error=process_incorrect_amount_for_new_event,
            type_factory=validate_amount_for_new_event
        ),
        Back(),
        state=states.AddFinanceEvent.ENTER_VALUE
    ),
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'Когда ты {finance_event_verb} эти деньги?'
        ),
        Calendar(
            id='fin_calendar',
            on_click=on_date_clicked,
            config=CalendarConfig(
                max_date=datetime.date.today()
            )
        ),
        Button(
            id='fin_today',
            text=Const('Сегодня'),
            on_click=on_today_clicked,
        ),
        Back(),

        state=states.AddFinanceEvent.CHOOSE_DATE,
    ),
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            '✅ {capitalized_finance_event_name} {dialog_data[value]} за {dialog_data[event_date]} успешно зарегистрирован.'  # TODO: Сделать красивый рендеринг для event_date и value
        ),
        state=states.AddFinanceEvent.FINAL
    ),
    getter=finance_event_words_getter,
)
