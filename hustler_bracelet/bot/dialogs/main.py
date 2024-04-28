from datetime import date, timedelta

from aiogram_dialog import Dialog, LaunchMode, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from . import states
from .finance.add_event import on_start_add_event_dialog_click
from ..utils.lang_utils import formatted_balance_getter
from ...enums import FinanceTransactionType
from ...managers.finance_manager import FinanceManager


async def main_dialog_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    async def get_tasks_for_today_and_tomorrow():
        all_tasks = await finance_manager.get_active_tasks()
        tasks_for_today = [
            task for task in all_tasks if task.planned_complete_date == date.today()
        ]
        tasks_for_today_amount = len(tasks_for_today)

        tasks_for_tomorrow = [
            task for task in all_tasks if task.planned_complete_date == date.today() + timedelta(days=1)
        ]
        tasks_for_tomorrow_amount = len(tasks_for_tomorrow)

        text = ''
        if tasks_for_today_amount == 0:
            text += '<b>📝 На сегодня у тебя нет задач.</b>\n\n'
        else:
            text += f'<b>📝 На сегодня у тебя {tasks_for_today_amount} задач:</b>\n'
            for task in tasks_for_today:
                text += f' •  {task.name}\n'
            text += '\n'

        if tasks_for_tomorrow_amount == 0:
            text += '<b>🕐 На завтра у тебя нет задач.</b>\n\n'
        else:
            text += f'<b>🕐 И ещё {tasks_for_tomorrow_amount} задач на завтра:</b>\n'
            for task in tasks_for_tomorrow:
                text += f' •  {task.name}\n'
            text += '\n'

        return text

    return {
        **await formatted_balance_getter(dialog_manager, **kwargs),
        'incomes_amount': await finance_manager.get_events_amount(FinanceTransactionType.INCOME),
        'spends_amount': await finance_manager.get_events_amount(FinanceTransactionType.SPENDING),
        'tasks_text': await get_tasks_for_today_and_tomorrow()
    }


main_dialog = Dialog(
    Window(
        Format(
            '👋 <b>Привет, хаслер!</b>\n'
            'Вот твоя сводка на сегодня:\n'
            '\n'
            '💵 <b>Твой капитал:</b> {balance}\n'
            '• Сегодня было {incomes_amount} прихода и {spends_amount} расходов\n'  # TODO: добавить склонение "прихода" и "расходов" 
            '\n'
            '{tasks_text}'
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
