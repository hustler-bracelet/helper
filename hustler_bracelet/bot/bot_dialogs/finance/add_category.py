from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.bot_dialogs import states
from hustler_bracelet.bot.lang_utils import finance_event_words_getter
from hustler_bracelet.enums import FinanceEventType


async def on_category_type_click(
        callback: ChatEvent,
        button: Button,
        manager: DialogManager
):
    manager.dialog_data['event_type'] = FinanceEventType(button.widget_id.split('_')[-1])

    await manager.next()


async def get_name_for_new_category(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: dict
):
    # TODO: Тут надо создать новую категорию. Название для неё лежит в message.text, а тип в dialog_manager.start_data['cat_type]

    await dialog_manager.done()


add_finance_category_dialog = Dialog(
    Window(
        Const('Какой тип будет иметь новая категория?'),
        Row(
            Button(
                text=Const('Доходы'),
                id='cat_type_income',
                on_click=on_category_type_click
            ),
            Button(
                text=Const('Расходы'),
                id='cat_type_spend',
                on_click=on_category_type_click
            )
        ),
        state=states.AddFinanceCategory.MAIN
    ),
    Window(
        Format('Какое имя будет у новой категории {finance_event_name}?'),
        TextInput(id='name_for_new_cat', on_success=get_name_for_new_category),
        state=states.AddFinanceCategory.ENTER_NAME
    ),
    getter=finance_event_words_getter,
)
