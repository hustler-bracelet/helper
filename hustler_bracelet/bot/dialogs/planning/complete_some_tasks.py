import operator

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Multiselect, Column, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states


async def get_tasks(**kwargs):
    return {
        'tasks': [
            ('Пинать хуи 1', 1),
            ('Пинать хуи 2', 2),
            ('Пинать хуи 3', 3),
            ('Пинать хуи 4', 4),
            ('Пинать хуи 5', 5),
            ('Пинать хуи 6', 6),
            ('Пинать хуи 7', 7),
            ('Пинать хуи 8', 8),
            ('Пинать хуи 9', 9),
            ('Пинать хуи 10', 10),
        ]
    }


async def on_complete_selected_tasks_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    tasks_multiselect_widget: Multiselect = manager.find('mltslct_tasks_to_complete')
    checked = tasks_multiselect_widget.get_checked()
    await callback.answer(', '.join(checked))


complete_some_tasks_dialog = Dialog(
    Window(
        Const(
            '✅ <b>Выполнение задач</b>\n'
            '\n'
            'Выбери задачи, которые хочешь отметить выполненными:'
        ),
        ScrollingGroup(
            Column(
                Multiselect(
                    Format("✓ {item[0]}"),
                    Format("{item[0]}"),
                    id="mltslct_tasks_to_complete",
                    item_id_getter=operator.itemgetter(1),
                    items="tasks",
                )
            ),
            id='scrl_tasks_to_complete',
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Row(
            Cancel(
                Const('❌ Отмена')
            ),
            Button(
                Const('✅ Выполнить'),
                id='complete_selected_tasks',
                on_click=on_complete_selected_tasks_click
            )
        ),
        state=states.CompleteSomeTasks.MAIN,
        getter=get_tasks
    )
)
