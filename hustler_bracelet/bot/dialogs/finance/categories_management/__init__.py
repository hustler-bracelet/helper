from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start, Cancel, Back
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.enums import FinanceTransactionType

finance_categories_management_menu_dialog = Dialog(
    Window(
        Const(
            '📁 <b>Управление категориями</b>\n'
            '\n'
            '↗️ <b>Твои категории доходов:</b>\n'
            'Телеграм ворк (2 500 000₽)\n'
            'Посредничество (100 000₽)\n'
            '\n'
            '↙️ <b>Твои категории расходов:</b>\n'
            'Новые айфоны (2 000 000₽)\n'
            'Золотое яблоко (50 000₽)'
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
        state=states.FinanceCategoriesManagementMenu.MAIN
    )
)
