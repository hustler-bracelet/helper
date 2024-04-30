from datetime import timedelta

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Start, Cancel, Button
from aiogram_dialog.widgets.text import Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.finance.add_event import on_start_add_event_dialog_click
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers.finance_manager import FinanceManager


async def finance_menu_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    balance = await finance_manager.get_balance()
    mp_income_category_name, mp_income_category_balance = await finance_manager.get_most_profitable_income_category()
    mp_spendings_category_name, mp_spendings_category_balance = await finance_manager.get_most_spending_category()
    sua_income_today, oc_income_today = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.INCOME,
        until_date=timedelta(days=0)
    )

    return {
        'balance': balance,
        'mp_income_category_name': mp_income_category_name,
        'mp_income_category_balance': mp_income_category_balance,
        'mp_spendings_category_name': mp_spendings_category_name,
        'mp_spendings_category_balance': mp_spendings_category_balance,
        'sua_income_today': sua_income_today,
        'oc_income_today': oc_income_today
    }


finance_menu_dialog = Dialog(
    Window(
        Jinja(
            # TODO: add plural
            '\n'
            '💸 <b>Финансы</b>\n'
            '\n'
            '💵 <b>Твой капитал:</b> {{ balance|money }}\n'
            '\n'
            '<b>↗ Доходы:</b>\n'
            '<b>• За сегодня:</b> {{ sua_income_today }} ({{ oc_income_today }} операции)\n'
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
            '<b>{{ mp_income_category_name}}</b> ({{ mp_income_category_balance }})\n'
            '\n'
            '💳 А больше всего расходов в категории:\n'
            '<b>{{ mp_spendings_category_name }}</b> ({{ mp_spendings_category_balance }})\n'
        ),
        Row(
            Button(
                text=Const('🤑 Добавить доход'),
                id='add_income',
                on_click=on_start_add_event_dialog_click(FinanceTransactionType.INCOME)
            ),
            Button(
                text=Const('💳 Добавить расход'),
                id='add_spend',
                on_click=on_start_add_event_dialog_click(FinanceTransactionType.SPENDING)
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
        Cancel(Const('❌ Отмена')),

        state=states.FinanceMainMenu.MAIN,
        getter=finance_menu_getter
    )
)
