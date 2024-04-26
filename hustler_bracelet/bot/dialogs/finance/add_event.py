import datetime
import operator
from datetime import date
from typing import Any

from aiogram import types, html
from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Calendar, ManagedCalendar, Button, ScrollingGroup, Back, CalendarConfig, Select, Cancel
)
from aiogram_dialog.widgets.text import Const, Format
from simpleeval import SimpleEval

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils.lang_utils import finance_event_words_getter
from hustler_bracelet.bot.dialogs.widgets import Today
from hustler_bracelet.database.exceptions import CategoryNotFoundError
from hustler_bracelet.finance.manager import FinanceManager

_evaluator = SimpleEval()


async def on_date_clicked(
        callback: ChatEvent,
        widget: ManagedCalendar | None,
        manager: DialogManager,
        selected_date: date
):
    await callback.answer(str(selected_date))
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']

    manager.dialog_data['event_date'] = selected_date  # Пригодится при форматировании финального сообщения

    try:
        category = await finance_manager.get_category_by_id(manager.dialog_data['category_id'])
    except CategoryNotFoundError:
        return  # TODO: Добавить реакцию на CategoryNotFoundError

    await finance_manager.add_finance_transaction(
        category,
        manager.dialog_data['value'],
        selected_date
    )

    await manager.next()


async def on_add_category_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.start(
        state=states.AddFinanceCategory.ENTER_NAME,  # Скипаем первый этап, т.к. ответ на первый вопрос (тип категории) уже известен
        data={
            'cat_type': manager.start_data['event_type'],
            'force_done': True
        }
    )


async def on_choose_category_click(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: int
):
    manager.dialog_data['category_id'] = item_id

    await manager.next()


async def category_choose_window_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']
    categories = await finance_manager.get_all_categories(dialog_manager.start_data['event_type'])
    print(categories)

    return {
        'categories': [(category.name, category.id) for category in categories]
    }


async def on_amount_for_new_event_entered(
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
    await message.answer('\n'.join([*map(html.quote, error.args), 'Попробуй ещё раз']))


def validate_amount_for_new_event(text: str):
    amount = text.lower()

    replace_mapping = {
        ' ': '',
        ',': '.',
        '^': '**',
        ':': '/'
    }
    for old, new in replace_mapping.items():
        amount = amount.replace(old, new)

    try:
        amount = _evaluator.eval(amount)
    except BaseException:
        raise ValueError('Кажется, ты ввёл неправильную формулу')

    return amount


async def on_process_result(
        start_data: dict,
        result_data: dict,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['category_id'] = result_data['category_id']
    await dialog_manager.next()


add_finance_event_dialog = Dialog(
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'Выбери категорию {finance_event_name}ов или создай новую:'
        ),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='select_categories_for_new_event',
                item_id_getter=operator.itemgetter(1),
                items='categories',
                on_click=on_choose_category_click
            ),
            id="scroll_categories_for_new_event",
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Button(text=Const('➕ Создать новую категорию'), id='add_fin_category', on_click=on_add_category_click),
        Cancel(),
        state=states.AddFinanceEvent.MAIN,
        getter=category_choose_window_getter
    ),
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'Введи сумму, которую ты {finance_event_verb} (в рублях):'
        ),
        TextInput(
            id='amount_of_new_event',
            on_success=on_amount_for_new_event_entered,
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
        Today(on_date_clicked),
        Back(),

        state=states.AddFinanceEvent.CHOOSE_DATE,
    ),
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            '✅ {capitalized_finance_event_name} {dialog_data[value]} за {dialog_data[event_date]} успешно зарегистрирован.'  # TODO: Сделать красивый рендеринг для event_date и value
        ),
        Cancel(Const('Ok')),
        state=states.AddFinanceEvent.FINAL
    ),
    getter=finance_event_words_getter,
    on_process_result=on_process_result
)
