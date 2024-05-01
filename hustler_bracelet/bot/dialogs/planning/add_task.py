import datetime
from datetime import date

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Cancel, Calendar, ManagedCalendar, CalendarConfig, Back
from aiogram_dialog.widgets.text import Const, Format, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.widgets import Today
from hustler_bracelet.managers import FinanceManager


async def on_name_for_new_task_entered(
        message: types.Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['name'] = message.text
    await dialog_manager.next()


async def on_date_clicked(
        callback: ChatEvent,
        widget: ManagedCalendar | None,
        manager: DialogManager,
        selected_date: date
):
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']

    manager.dialog_data['date'] = selected_date

    await finance_manager.add_task(
        name=manager.dialog_data['name'],
        planned_complete_date=selected_date
    )

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
        Cancel(Const('❌ Отмена')),
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
        Back(Const('⬅️ Назад')),
        state=states.AddTask.GET_DATE
    ),
    Window(
        Jinja(
            '➕ <b>Добавление задачи</b>\n'
            '\n'
            '✅ Задача “{{ dialog_data[\'name\'] }}” на {{ dialog_data[\'date\']|date }} успешно добавлена.'
        ),
        Cancel(Const('👌 Ок')),
        state=states.AddTask.FINAL
    )
)
