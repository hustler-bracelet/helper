from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Start, Cancel
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils.lang_utils import formatted_balance_getter
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.finance.manager import FinanceManager


finance_menu_dialog = Dialog(
    Window(
        Format(
            '\n'
            '💸 <b>Финансы</b>\n'
            '\n'
            '💵 <b>Твой капитал:</b> {balance}\n'
            '\n'
            '<b>↗ Доходы:</b>\n'
            '<b>• За сегодня:</b> 5 000₽ (2 операции)\n'
            '<b>• За неделю:</b> 20 000₽ (5 операций)\n'
            '<b>• За месяц:</b> 75 000₽ (27 операций)\n'
            '\n'
            '<b>↙️ Расходы:</b>\n'
            '<b>• За сегодня:</b> 0₽\n'
            '<b>• За неделю:</b> 10 000₽ (1 операция)\n'
            '<b>• За месяц:</b> 15 000₽ (2 операции)\n'
            '\n'
            '📈 <b>Твои активы:</b>\n'
            '<b>• Нак. счёт Тинькофф:</b> 215 000₽ (15%, прибыль: 15 000₽)\n'
            '<b>• Браслет токен:</b> 52 812₽ (прибыль: 2 812₽)\n'
            '\n'
            '🤑 Самый большой доход у тебя в категории:\n'
            '<b>Телеграм ворк</b> (250 000₽)\n'
            '💳 А больше всего расходов в категории:\n'
            '<b>Новые айфоны</b> (2 000 000₽)\n'
        ),
        Row(
            Start(
                text=Const("🤑 Добавить доход"),
                id="add_income",
                state=states.AddFinanceEvent.MAIN,
                data={'event_type': FinanceTransactionType.INCOME}
            ),
            Start(
                text=Const("💳 Добавить расход"),
                id="add_spend",
                state=states.AddFinanceEvent.MAIN,
                data={'event_type': FinanceTransactionType.SPENDING}
            ),
        ),
        Start(
            text=Const('📂 Управление категориями'),
            id='categories_management_menu',
            state=states.FinanceCategoriesManagementMenu.MAIN
        ),
        Start(
            text=Const('📈 Инвестиции'),
            id='investments_management_menu',
            state=states.FinanceInvestmentsMenu.MAIN
        ),
        Cancel(),

        state=states.FinanceMainMenu.MAIN,
        getter=formatted_balance_getter
    )
)
