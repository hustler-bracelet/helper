from datetime import timedelta
from typing import Sequence

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Start, Cancel, Button
from aiogram_dialog.widgets.text import Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.finance.add_event import on_start_add_event_dialog_click
from hustler_bracelet.database.asset import Asset
from hustler_bracelet.enums import FinanceTransactionType
from hustler_bracelet.managers.finance_manager import FinanceManager


async def finance_menu_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    balance = await finance_manager.get_balance()
    mp_income_category_name, mp_income_category_balance = await finance_manager.get_most_profitable_income_category()
    mp_spendings_category_name, mp_spendings_category_balance = await finance_manager.get_most_spending_category()

    sua_income_today, oc_income_today = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.INCOME,
        until_date=timedelta(0)
    )
    sua_income_week, oc_income_week = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.INCOME,
        until_date=timedelta(7)
    )
    sua_income_month, oc_income_month = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.INCOME,
        until_date=timedelta(30)
    )

    sua_spendings_today, oc_spendings_today = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.SPENDING,
        until_date=timedelta(0)
    )
    sua_spendings_week, oc_spendings_week = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.SPENDING,
        until_date=timedelta(7)
    )
    sua_spendings_month, oc_spendings_month = await finance_manager.get_stats_for_time_range(
        type_=FinanceTransactionType.SPENDING,
        until_date=timedelta(30)
    )

    assets: Sequence[Asset] = await finance_manager.get_all_assets()

    return {
        'balance': balance,
        'mp_income_category_name': mp_income_category_name,
        'mp_income_category_balance': mp_income_category_balance,
        'mp_spendings_category_name': mp_spendings_category_name,
        'mp_spendings_category_balance': mp_spendings_category_balance,

        'sua_income_today': sua_income_today,
        'oc_income_today': oc_income_today,
        'sua_income_week': sua_income_week,
        'oc_income_week': oc_income_week,
        'sua_income_month': sua_income_month,
        'oc_income_month': oc_income_month,

        'sua_spendings_today': sua_spendings_today,
        'oc_spendings_today': oc_spendings_today,
        'sua_spendings_week': sua_spendings_week,
        'oc_spendings_week': oc_spendings_week,
        'sua_spendings_month': sua_spendings_month,
        'oc_spendings_month': oc_spendings_month,

        'assets': {
            asset.name:
                (asset.current_amount, asset.interest_rate, asset.current_amount - asset.base_amount)
            for asset in assets
        }
    }  # TODO: what the fuck?


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
            '<b>• За сегодня:</b> {{ sua_income_today|money }} ({{ oc_income_today }} операций)\n'
            '<b>• За неделю:</b> {{ sua_income_week|money }} ({{ oc_income_week }} операций)\n'
            '<b>• За месяц:</b> {{ sua_income_month|money }} ({{ oc_income_month }} операций)\n'
            '\n'
            '<b>↙️ Расходы:</b>\n' 
            '<b>• За сегодня:</b> {{ sua_spendings_today|money }} ({{ oc_spendings_today }} операций)\n'
            '<b>• За неделю:</b> {{ sua_spendings_week|money }} ({{ oc_spendings_week }} операций)\n'
            '<b>• За месяц:</b> {{ sua_spendings_month|money }} ({{ oc_spendings_month }} операции)\n'
            '\n'
            '📈 <b>Твои активы:</b>\n'
            '{% for name, details in assets.items() %}'
            ' •  <b>{{ name }}:</b> {{ details[0]|money }}'
            '{% if details[1] is not none %} ({{ details[1]|number }}%, прибыль: {{ details[2]|money }})\n'
            '{% else %} (прибыль: {{ details[2]|money }}₽)\n'
            '{% endif %}'
            '{% endfor %}\n'
            '\n'
            '🤑 Самый большой доход у тебя в категории:\n'
            '<b>{{ mp_income_category_name}}</b> ({{ mp_income_category_balance|money }})\n'
            '\n'
            '💳 А больше всего расходов в категории:\n'
            '<b>{{ mp_spendings_category_name }}</b> ({{ mp_spendings_category_balance|money }})\n'
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
            text=Const('📈 Инвестиции β'),
            id='investments_management_menu',
            state=states.FinanceInvestmentsMenu.MAIN
        ),
        Cancel(Const('❌ Отмена')),

        state=states.FinanceMainMenu.MAIN,
        getter=finance_menu_getter
    )
)
