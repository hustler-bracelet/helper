from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row
from aiogram_dialog.widgets.text import Const, Format

from . import states
from ...enums import FinanceTransactionType
from ...finance.manager import FinanceManager


async def main_dialog_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'balance': await finance_manager.get_balance(),
        'incomes_amount': await finance_manager.get_events_amount(FinanceTransactionType.INCOME),
        'spends_amount': await finance_manager.get_events_amount(FinanceTransactionType.SPENDING)
    }


main_dialog = Dialog(
    Window(
        Format(
            '👋 <b>Привет, хаслер!</b>\n'
            'Вот твоя сводка на сегодня:\n'
            '\n'
            '💵 <b>Твой капитал:</b> {balance}₽\n'
            '• Сегодня было {incomes_amount} прихода и {spends_amount} расходов\n'  # TODO: добавить склонение "прихода" и "расходов" 
            '\n'
            '📝 <b>2 задачи на сегодня:</b>\n'
            '• Налить трафа Ване\n'
            '• Вынести мусор\n'
            '\n'
            '🕔 <b>И ещё 1 задача на завтра:</b>\n'
            '• Инвайт на фотостудию\n'
        ),
        # Start(
        #     text=Const("📐 Layout widgets"),
        #     id="layout",
        #     state=states.Layouts.MAIN,
        # ),
        # Start(
        #     text=Const("📜 Scrolling widgets"),
        #     id="scrolls",
        #     state=states.Scrolls.MAIN,
        # ),
        # Start(
        #     text=Const("☑️ Selection widgets"),
        #     id="selects",
        #     state=states.Selects.MAIN,
        # ),
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
        Start(
            text=Const("📝 Добавить задачу"),
            id="add_task",
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
                id='tasktracking_menu',
                state=states.TaskTracking.MAIN
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
        # Start(
        #     text=Const("💯 Counter and Progress"),
        #     id="counter",
        #     state=states.Counter.MAIN,
        # ),
        # Start(
        #     text=Const("🎛 Combining widgets"),
        #     id="multiwidget",
        #     state=states.Multiwidget.MAIN,
        # ),
        # Start(
        #     text=Const("🔢 Multiple steps"),
        #     id="switch",
        #     state=states.Switch.MAIN,
        # ),
        # Start(
        #     text=Const("⌨️ Reply keyboard"),
        #     id="reply",
        #     state=states.ReplyKeyboard.MAIN,
        # ),
        state=states.Main.MAIN,
        getter=main_dialog_getter
    ),
    launch_mode=LaunchMode.ROOT,
)
