from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.bot_dialogs import states

task_tracking_main_menu_dialog = Dialog(
    Window(
        Const(
            '✅ Планирование\n'
            '\n'
            '📝 2 задачи на сегодня:\n'
            'Налить трафа Ване\n'
            'Вынести мусор\n'
            '\n'
            '🕐 1 задача на завтра: \n'
            'Инвайт на фотостудию\n'
            '\n'
            '📆 1 задача на 30 апреля:\n'
            'Сдать бота Амби\n'
            '\n'
            '💪 У тебя 4 задачи к выполнению. Поворкаем?\n'
            '\n'
            '📊 Ты закрыл уже 294 задачи. Неплохо!'
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
        state=states.TaskTracking.MAIN
    )
)
