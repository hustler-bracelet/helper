from datetime import date, timedelta

from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from . import states
from .finance.add_event import on_start_add_event_dialog_click
from .planning import get_jinja_widget_for_tasks_displaying, get_planning_data_getter
from ..utils.lang_utils import formatted_balance_getter
from ...enums import FinanceTransactionType
from ...managers.finance_manager import FinanceManager


async def main_dialog_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        **await formatted_balance_getter(dialog_manager, **kwargs),
        'incomes_amount': await finance_manager.get_events_amount(FinanceTransactionType.INCOME),
        'spends_amount': await finance_manager.get_events_amount(FinanceTransactionType.SPENDING)
    }


main_dialog = Dialog(
    Window(
        Format(
            '👋 <b>Привет, хаслер!</b>\n'
            'Вот твоя сводка на сегодня:\n'
            '\n'
            '💵 <b>Твой капитал:</b> {balance}\n'
            '• Сегодня было {incomes_amount} прихода и {spends_amount} расходов'  # TODO: добавить склонение "прихода" и "расходов"'
        ),
        get_jinja_widget_for_tasks_displaying(),
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
        Start(
            text=Const('📝 Добавить задачу'),
            id='add_task',
            state=states.AddTask.MAIN
        ),
        Row(
            Start(
                text=Const('💸 Финансы'),
                id='finance_control_menu',
                state=states.FinanceMainMenu.MAIN
            ),
            Start(
                text=Const('✅ Планирование'),
                id='planning_menu',
                state=states.Planning.MAIN
            ),
            Start(
                text=Const('💪 Спорт'),
                id='sport_menu',
                state=states.Sport.MAIN
            )
        ),
        Start(
            text=Const('⚙️ Настройки'),
            id='setting_menu',
            state=states.SettingsMainMenu.MAIN
        ),
        state=states.Main.MAIN,
        getter=(main_dialog_getter, get_planning_data_getter(include_other_days=False)),
    ),
    launch_mode=LaunchMode.ROOT,
)
