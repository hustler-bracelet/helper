from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Start, Cancel, Back
from aiogram_dialog.widgets.text import Const, List, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils.lang_utils import format_money_amount
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers import FinanceManager


async def finance_categories_management_menu_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'income_list': [
            (
                await category.awaitable_attrs.name,
                format_money_amount(await finance_manager.get_sum_of_finance_transactions_of_category(category))
            ) for category in
            await finance_manager.get_all_categories(FinanceTransactionType.INCOME)
        ],
        'spending_list': [
            (
                await category.awaitable_attrs.name,
                format_money_amount(await finance_manager.get_sum_of_finance_transactions_of_category(category))
            ) for category in
            await finance_manager.get_all_categories(FinanceTransactionType.SPENDING)
        ],
    }


finance_categories_management_menu_dialog = Dialog(
    Window(
        Const(
            '📁 <b>Управление категориями</b>\n'
            '\n'
            '↗️ <b>Твои категории доходов:</b>'),
        List(
            Format(' •  {item[0]} ({item[1]})'),
            items='income_list'
        ),
        Const(
            '\n'
            '↙️ <b>Твои категории расходов:</b>'
        ),
        List(
            Format(' •  {item[0]} ({item[1]})'),
            items='spending_list'
        ),
        Row(
            Start(
                text=Const("🗑 Удалить"),
                id="delete_finance_category",
                state=states.DeleteFinanceCategory.MAIN
            ),
            Start(
                text=Const("➕ Добавить"),
                id="create_finance_category",
                state=states.AddFinanceCategory.MAIN
            ),
        ),
        Cancel(),
        state=states.FinanceCategoriesManagementMenu.MAIN,
        getter=finance_categories_management_menu_getter
    )
)
