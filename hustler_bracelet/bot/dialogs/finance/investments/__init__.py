from datetime import timedelta, date
from typing import Sequence

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.utils.lang_utils import plural_form, represent_date
from hustler_bracelet.database.asset import Asset
from hustler_bracelet.database.investment_transaction import InvestmentTransaction
from hustler_bracelet.managers import FinanceManager


async def investments_data_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    assets: Sequence[Asset] = await finance_manager.get_all_assets()
    investment_transactions: Sequence[InvestmentTransaction] = await finance_manager.get_investment_transactions()

    def get_asset_name_by_id(asset_id: int) -> str:
        for asset in assets:
            if asset.id == asset_id:
                return asset.name
        return '???'

    def calculate_percentage(a: float, b: float):
        return float(round(a/b * 100, 1))

    return {
        'assets': {
            asset.name:
                (asset.current_amount, asset.interest_rate, asset.current_amount - asset.base_amount)
            for asset in assets
        },
        'investment_transactions': {
            get_asset_name_by_id(investment_transaction.asset_id):
                (investment_transaction.added_on.date(), investment_transaction.value)
            for investment_transaction in investment_transactions
        },
        'money_in_assets_amount': await finance_manager.get_all_money_in_assets(),
        'money_in_assets_percent': calculate_percentage(
            await finance_manager.get_all_money_in_assets(),
            await finance_manager.get_balance()
        ),
    }


def get_jinja_widget_for_assets_displaying() -> Jinja:
    return Jinja(
        '{% for name, details in assets.items() %}'
        ' •  <b>{{ name }}:</b> {{ details[0]|money }}'
        '{% if details[1] is not none %} ({{ details[1]|number }}%, прибыль: {{ details[2]|money }})\n'
        '{% else %} (прибыль: {{ details[2]|money }}₽)\n'
        '{% endif %}'
        '{% endfor %}'
    )


def get_jinja_widget_for_investment_transactions_displaying() -> Jinja:
    return Jinja(
        '{% for name, (date, value) in investment_transactions.items() %}\n'
        ' •  {{ date|date }} + {{ value|money }} по активу {{ name }}\n'
        '{% endfor %}'
    )


investments_main_menu_dialog = Dialog(
    Window(
        Jinja(
            '📊 <b>Инвестиции</b> (beta)\n'
            '\n'
            '💵 <b>Всего в активах:</b> {{ money_in_assets_amount|money }}\n'
            '🧮 Твой капитал на {{ money_in_assets_percent }}% состоит из активов\n'
            '\n'
            '📈 <b>Твои активы:</b>'
        ),
        get_jinja_widget_for_assets_displaying(),
        Const(
            '🕐 <b>История зачислений:</b>'
        ),
        get_jinja_widget_for_investment_transactions_displaying(),
        Start(
            Const('🤑 Добавить прибыль'),
            id='add_asset_income',
            state=states.AddInvestmentProfit.MAIN
        ),
        Row(
            Start(
                Const('➕ Добавить актив'),
                id='add_asset',
                state=states.AddFinanceAsset.MAIN
            ),
            Start(
                Const('➖ Удалить актив'),
                id='delete_asset',
                state=states.DeleteAssets.MAIN
            ),
        ),
        Row(
            Start(
                Const('✏️ Переим. актив'),
                id='rename_asset',
                state=states.RenameAsset.MAIN
            ),
            Start(
                Const('🧮 Изменить % ставку'),
                id='change_asset_percent',
                state=states.ChangeInterestRate.MAIN
            ),
        ),
        Cancel(Const('❌ Отмена')),
        state=states.FinanceInvestmentsMenu.MAIN,
        getter=investments_data_getter,
    )
)
