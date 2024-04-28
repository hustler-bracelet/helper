from datetime import date, timedelta

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager
from hustler_bracelet.database.task import Task


async def planning_main_menu_statistic_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    async def get_all_tasks_text():
        all_tasks = await finance_manager.get_active_tasks()

        tasks_for_today = [
            task for task in all_tasks if task.planned_complete_date == date.today()
        ]
        tasks_for_today_amount = len(tasks_for_today)

        tasks_for_tomorrow = [
            task for task in all_tasks if task.planned_complete_date == date.today() + timedelta(days=1)
        ]
        tasks_for_tomorrow_amount = len(tasks_for_tomorrow)

        all_tasks = [task for task in all_tasks if task not in tasks_for_today and task not in tasks_for_tomorrow]

        other_tasks_sorted: dict[date, list[Task]] = {}
        for task in all_tasks:
            if task.planned_complete_date not in other_tasks_sorted.keys():
                other_tasks_sorted[task.planned_complete_date] = []
            other_tasks_sorted[task.planned_complete_date].append(task)

        text = ''
        if tasks_for_today_amount == 0:
            text += '📝 На сегодня нет задач.\n\n'
        else:
            text += f'📝 {tasks_for_today_amount} задач на сегодня:\n'
            for task in tasks_for_today:
                text += f' •  {task.name}\n'
            text += '\n'

        if tasks_for_tomorrow_amount == 0:
            text += '🕐  На завтра нет задач.\n\n'
        else:
            text += f'🕐 {tasks_for_tomorrow_amount} задач на завтра:\n'
            for task in tasks_for_tomorrow:
                text += f' •  {task.name}\n'
            text += '\n'

        if not other_tasks_sorted:
            pass
        else:
            for date_, tasks_for_this_date in other_tasks_sorted.items():
                tasks_for_this_date_amount = len(tasks_for_this_date)
                text += f'📆 {tasks_for_this_date_amount} задач на {date_}:\n'
                for task in tasks_for_this_date:
                    text += f' •  {task.name}\n'
                text += '\n'

        return text

    return {
        'all_tasks': await get_all_tasks_text(),
        'today_uncompleted_tasks_amount': await finance_manager.get_amount_of_tasks_filtered_by_planned_complete_date(
            date.today(),
            completed=False
        ),
        'tomorrow_uncompleted_tasks_amount': await finance_manager.get_amount_of_tasks_filtered_by_planned_complete_date(
            date.today() + timedelta(days=1),
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
            '{all_tasks}'
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
