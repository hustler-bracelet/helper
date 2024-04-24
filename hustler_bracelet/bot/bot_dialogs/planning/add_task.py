import datetime
from datetime import date

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel, Calendar, ManagedCalendar, CalendarConfig, Back
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.bot_dialogs import states
from hustler_bracelet.bot.widgets import Today


async def on_name_for_new_task_entered(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['task_name'] = message.text
    await dialog_manager.next()


async def on_date_clicked(
        callback: ChatEvent,
        widget: ManagedCalendar | None,
        manager: DialogManager,
        selected_date: date
):
    manager.dialog_data['task_date'] = selected_date
    await manager.next()


add_task_dialog = Dialog(
    Window(
        Const(
            '➕ <b>Добавление задачи</b>\n'
            '\n'
            'Какую задачу тебе нужно выполнить?'
        ),
        TextInput(
            id='enter_name_for_new_task',
            on_success=on_name_for_new_task_entered
        ),
        Cancel(),
        state=states.AddTask.MAIN
    ),
    Window(
        Const(
            '➕ <b>Добавление задачи</b>\n'
            '\n'
            'Когда тебе нужно выполнить эту задачу?'
        ),
        Calendar(
            id='tasks_calendar',
            on_click=on_date_clicked,
            config=CalendarConfig(
                min_date=datetime.date.today()
            )
        ),
        Today(on_date_clicked),
        Back(),
        state=states.AddTask.GET_DATE
    ),
    Window(
        Format(
            '➕ <b>Добавление задачи</b>\n'
            '\n'
            '✅ Задача “{dialog_data[task_name]}” на {dialog_data[task_date]} успешно добавлена. (нет)'
        ),
        Cancel(Const('Ok')),
        state=states.AddTask.FINAL
    )
)
