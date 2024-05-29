from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Jinja

from . import states
from .planning import get_jinja_widget_for_tasks_displaying, get_planning_data_getter
from ...enums import FinanceTransactionType
from ...managers.finance_manager import FinanceManager


async def main_dialog_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'balance': await finance_manager.get_balance(),
        'incomes_amount': await finance_manager.get_events_amount(FinanceTransactionType.INCOME),
        'spends_amount': await finance_manager.get_events_amount(FinanceTransactionType.SPENDING)
    }


main_dialog = Dialog(
    Window(
        Jinja(
            '👋 <b>Привет, хаслер!</b>\n'
            'Вот твоя сводка на сегодня:\n'
            '\n'
            '💵 <b>Твой капитал:</b> {{ balance | money }}\n'
            '• Сегодня было {{ incomes_amount|plural(["поступление", "поступления", "поступлений"]) }} '
            'и {{ spends_amount|plural(["расход", "расхода", "расходов"]) }}'
        ),
        get_jinja_widget_for_tasks_displaying(),
        Start(
            text=Const('🤑 Добавить доход'),
            id='add_income',
            state=states.AddFinanceEvent.MAIN,
            data={'event_type': FinanceTransactionType.INCOME}
        ),
        Start(
            text=Const('💳 Добавить расход'),
            id='add_spend',
            state=states.AddFinanceEvent.MAIN,
            data={'event_type': FinanceTransactionType.SPENDING},
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
            text=Const('💰 Сезон крипты'),  # TODO: get from activity name
            id='activity_menu',
            state=states.Activity.MAIN
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
