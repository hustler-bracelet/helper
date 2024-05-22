from typing import Any

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.finance.widgets import get_choose_category_type_kb
from hustler_bracelet.bot.utils import get_event_type
from hustler_bracelet.bot.utils.lang_utils import finance_event_words_getter
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers.finance_manager import FinanceManager


async def on_category_type_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
):
    manager.dialog_data['event_type'] = FinanceTransactionType(item_id.upper())

    await manager.next()


async def get_name_for_new_category(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: dict
):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    new_category = await finance_manager.create_new_category(
        message.text,
        get_event_type(dialog_manager)
    )

    if dialog_manager.start_data and dialog_manager.start_data.get('force_done'):
        await dialog_manager.done(
            result={
                'category_id': await new_category.awaitable_attrs.id,
            }
        )
        return

    dialog_manager.dialog_data['category_id'] = await new_category.awaitable_attrs.id
    await dialog_manager.next()


async def on_cancel_click(
        callback: types.CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.done(
        result={
            'category_id': dialog_manager.dialog_data['category_id'],
        }
    )


add_finance_category_dialog = Dialog(
    Window(
        Format(
            '{finance_event_emoji} <b>Добавление {finance_event_name}а</b>\n'
            '\n'
            'У тебя нет ни одной категории {finance_event_name}а.\n'
            'Введи название категории, от которой поступил {finance_event_name}, и я её создам'
        ),
        TextInput(id='name_for_new_cat', on_success=get_name_for_new_category),
        Cancel(
            Const('❌ Отмена'),
               result={'fucked_up_on_the_category_creating': True}
        ),
        state=states.AddFinanceCategory.ENTER_NAME_FROM_EVENT_ADDING,
        getter=finance_event_words_getter
    ),
    Window(
        Const(
            '➕ <b>Добавление категории</b>\n'
            '\n'
            'Какой тип будет иметь новая категория?'
        ),
        get_choose_category_type_kb(on_category_type_selected),
        Cancel(Const('❌ Отмена')),
        state=states.AddFinanceCategory.MAIN
    ),
    Window(
        Format(
            '➕ <b>Добавление категории {finance_event_name}ов</b>\n'
            '\n'
            'Какое имя будет у новой категории {finance_event_name}ов?'
        ),
        TextInput(id='name_for_new_cat', on_success=get_name_for_new_category),
        Back(Const('⬅️ Назад')),
        state=states.AddFinanceCategory.ENTER_NAME,
        getter=finance_event_words_getter
    ),
    Window(
        Format(
            '➕ <b>Добавление категории {finance_event_name}ов</b>\n'
            '\n'
            'Категория успешно добавлена'
        ),
        Button(
            Const('👌 Ок'),
            on_click=on_cancel_click,
            id='on_cancel_id_while_category_created'
        ),
        state=states.AddFinanceCategory.FINAL,
        getter=finance_event_words_getter,
    ),
)
