import datetime

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def planning_main_menu_statistic_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'today_uncompleted_tasks_amount': await finance_manager.get_amount_of_tasks_filtered_by_planned_complete_date(
            datetime.date.today(),
            completed=False
        ),
        'tomorrow_uncompleted_tasks_amount': await finance_manager.get_amount_of_tasks_filtered_by_planned_complete_date(
            datetime.date.today() + datetime.timedelta(days=1),
            completed=False
        ),
        'uncompleted_tasks_amount': await finance_manager.get_amount_of_tasks(completed=False),
        'completed_tasks_amount': await finance_manager.get_amount_of_tasks(completed=True),
    }


planning_main_menu_dialog = Dialog(
    Window(
        Format(
            '✅ Планирование\n'
            '\n'
            '📝 {today_uncompleted_tasks_amount} задач на сегодня:\n'
            ' •  Налить трафа Ване\n'
            ' •  Вынести мусор\n'
            '\n'
            '🕐 {tomorrow_uncompleted_tasks_amount} задач на завтра: \n'
            ' •  Инвайт на фотостудию\n'
            '\n'
            '📆 1 задача на 30 апреля:\n'
            ' •  Сдать бота Амби\n'
            '\n'
            '💪 У тебя {uncompleted_tasks_amount} задач к выполнению. Поворкаем?\n'
            '\n'
            '📊 Ты закрыл уже {completed_tasks_amount} задач. Неплохо!'
        ),
        Start(
            text=Const('➕ Добавить задачу'),
            id='add_task',
            state=states.AddTask.MAIN
        ),
        Start(
            text=Const('✅ Выполнить задачи'),
            id='complete_some_tasks',
            state=states.CompleteSomeTasks.MAIN
        ),
        Cancel(),
        state=states.Planning.MAIN,
        getter=planning_main_menu_statistic_getter
    )
)
