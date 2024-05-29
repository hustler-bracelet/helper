import operator

from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Multiselect, Column, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def tasks_getter(dialog_manager: DialogManager, **kwargs):
    finance_manager: FinanceManager = dialog_manager.middleware_data['finance_manager']

    return {
        'tasks': [
            (await task.awaitable_attrs.name, await task.awaitable_attrs.id)
            for task in await finance_manager.get_tasks_sorted_by_planned_complete_date()
            # TODO: Добавить прогрузку задач по частям, чтобы не грузить каждый раз все сто тыщ мильонов тасок
        ]
    }


async def on_complete_selected_tasks_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    finance_manager: FinanceManager = manager.middleware_data['finance_manager']
    tasks_multiselect_widget: Multiselect = manager.find('mltslct_tasks_to_complete')
    completed_tasks_ids: list[int] = [*map(int, tasks_multiselect_widget.get_checked())]

    if not completed_tasks_ids:
        await callback.answer('Выберите хотя-бы одну задачу')
        return

    await finance_manager.mark_tasks_as_completed(completed_tasks_ids)

    await manager.done()


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
        getter=tasks_getter
    )
)
