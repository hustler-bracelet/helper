from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils import get_event_type
from hustler_bracelet.bot.utils.lang_utils import finance_event_words_getter
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


async def on_category_type_click(
        callback: ChatEvent,
        button: Button,
        manager: DialogManager
):
    manager.dialog_data['event_type'] = FinanceTransactionType(button.widget_id.split('_')[-1])

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
        await dialog_manager.done(result={'category_id': await new_category.awaitable_attrs.id})
        return

    dialog_manager.dialog_data['category_id'] = await new_category.awaitable_attrs.id
    await dialog_manager.next()


async def on_cancel_click(
        callback: types.CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.done(result={'category_id': dialog_manager.dialog_data['category_id']})


add_finance_category_dialog = Dialog(
    Window(
        Const(
            '➕ <b>Добавление категории</b>\n'
            '\n'
            'Какой тип будет иметь новая категория?'
        ),
        Row(
            Button(
                text=Const('Доходы'),
                id='cat_type_income',
                on_click=on_category_type_click
            ),
            Button(
                text=Const('Расходы'),
                id='cat_type_spending',
                on_click=on_category_type_click
            )
        ),
        state=states.AddFinanceCategory.MAIN
    ),
    Window(
        Format(
            '➕ <b>Добавление категории {finance_event_name}ов</b>\n'
            '\n'
            'Какое имя будет у новой категории {finance_event_name}ов?'
        ),
        TextInput(id='name_for_new_cat', on_success=get_name_for_new_category),
        state=states.AddFinanceCategory.ENTER_NAME,
        getter=finance_event_words_getter,
    ),
    Window(
        Format(
            '➕ <b>Добавление категории {finance_event_name}ов</b>\n'
            '\n'
            'Категория успешно добавлена'
        ),
        Button(
            Const('Ok'),
            on_click=on_cancel_click,
            id='on_cancel_id_while_category_created'
        ),
        state=states.AddFinanceCategory.FINAL,
        getter=finance_event_words_getter,
    ),
)
