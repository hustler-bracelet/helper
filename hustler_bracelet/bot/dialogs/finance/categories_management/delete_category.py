from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.finance.widgets import get_choose_category_type_kb, get_choose_category_kb
from hustler_bracelet.bot.utils.lang_utils import finance_event_words_getter
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


async def on_category_type_selected(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
):
    manager.dialog_data['cat_type'] = FinanceTransactionType(item_id)

    await manager.next()


async def on_choose_category_click(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: int
):
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']
    category = await finance_manager.get_category_by_id(item_id)
    manager.dialog_data['cat_name'] = await category.awaitable_attrs.name

    await finance_manager.delete_category(category)

    await manager.next()


async def category_choose_window_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']
    categories = await finance_manager.get_all_categories(dialog_manager.dialog_data['cat_type'])

    return {
        'categories': [(category.name, category.id) for category in categories]
    }


delete_finance_category_dialog = Dialog(
    Window(
        Format(
            '🗑 <b>Удаление категории</b>\n'
            '\n'
            'Категорию какого типа ты хочешь удалить?'
        ),
        get_choose_category_type_kb(on_category_type_selected),
        Cancel(),
        state=states.DeleteFinanceCategory.MAIN,
    ),
    Window(
        Format(
            '🗑 <b>Удаление категории {finance_event_name}ов</b>\n'
            '\n'
            'Выбери категорию {finance_event_name}ов, котору хочешь удалить'
        ),
        get_choose_category_kb(on_choose_category_click),
        Back(),
        state=states.DeleteFinanceCategory.CHOOSE_CATEGORY,
        getter=(
            category_choose_window_getter,
            finance_event_words_getter
        ),
    ),
    Window(
        Format(
            '🗑 <b>Удаление категории {finance_event_name}ов</b>\n'
            '\n'
            'Категория {finance_event_name}ов "{dialog_data[cat_name]}" успешно удалена'
        ),
        Cancel(Const('Ok')),
        state=states.DeleteFinanceCategory.FINAL,
        getter=finance_event_words_getter
    )
)
