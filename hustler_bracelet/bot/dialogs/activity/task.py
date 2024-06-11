import datetime
import random

from aiogram import F, types

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Start, Next, Back
from aiogram_dialog.widgets.text import Format, Jinja, Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.activity import activity_getter, activity_task_getter

from hustler_bracelet.client import ActivityTasksAPIClient


tasks_client = ActivityTasksAPIClient()

# async def on_process_result(
#         start_data: dict,
#         result_data: dict,
#         dialog_manager: DialogManager
# ):
#     pass


async def on_complete_activity_task_click(
        callback,
        widget,
        dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    await dialog_manager.start(
        states.ActivityTaskCompletion.MAIN,
        data={
            'activity_summary': data['activity_summary'],
        }
    )


async def on_cancel_task_click(
        callback,
        widget,
        dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary = data['activity_summary']

    await tasks_client.cancel_task(
        user_id=callback.from_user.id,
        task_id=activity_summary.niche.task.id,
    )

    await dialog_manager.next()


async def on_fucking_start_activity(
    start_data: dict, manager: DialogManager
):
    tasks = start_data.get('tasks')
    activity_summary = start_data.get('activity_summary')

    next_page = start_data.get('next_page')
    prev_page = start_data.get('prev_page')

    if tasks is not None and (
        prev_page is not None or next_page is not None
    ):
        manager.dialog_data.update({
            'tasks': tasks,
            'next_page': next_page,
            'prev_page': prev_page,
            'activity_summary': activity_summary,
        })
        return

    tasks = await tasks_client.get_all_tasks(
        user_id=manager.event.from_user.id,
        niche_id=start_data['activity_summary'].niche.id,
    )

    if not tasks:
        await manager.done()

    manager.dialog_data.update({
        'tasks': tasks,
        'activity_summary': activity_summary,
    })

    print(f"TASKS LEN - {len(tasks)}")

    if len(tasks) != 1:
        manager.dialog_data.update({
            'next_page': 1,
        })


async def govnocode_pagination(
    callback: types.CallbackQuery,
    widget,
    dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    tasks = data.get('tasks', [])
    activity_summary = data.get('activity_summary', None)

    next_page = data.get('next_page', 0)
    prev_page = data.get('prev_page', 0)

    current_page = 0

    print(callback.data)

    if callback.data == 'GOVNOCODE_PREV_TASK':
        current_page = prev_page

    else:
        current_page = next_page

    next_page = min(current_page + 1, len(tasks) - 1)
    prev_page = max(current_page - 1, 0)

    if current_page == 0:
        prev_page = None

    if current_page == len(tasks) - 1:
        next_page = None

    print(f'NEXT PAGE - {next_page}, PREV PAGE - {prev_page}')

    activity_summary.niche.task = tasks[current_page]

    await dialog_manager.start(
        states.ActivityTask.MAIN,
        data={
            'tasks': tasks,
            'next_page': next_page,
            'prev_page': prev_page,
            'activity_summary': activity_summary,
        }
    )


async def on_back_to_activity_click(
    callback,
    widget,
    dialog_manager: DialogManager
):
    await dialog_manager.start(
        states.Activity.MAIN,
        data={
            'activity_id': dialog_manager.dialog_data['activity_summary'].id,
        }
    )


async def pagination_getter(
    dialog_manager: DialogManager, **kwargs
):
    return {
        'next_page': dialog_manager.dialog_data.get('next_page'),
        'prev_page': dialog_manager.dialog_data.get('prev_page'),
    }


activity_task_dialog = Dialog(
    Window(
        Jinja(
            '{{task_emoji}} <b>{{task_name}}</b>\n'
            '\n'
            '{{task_caption}}\n'
            '\n'
            '🕐 <b>Задание выдано:</b> {{ task_sent_at|datetime }}\n'
            '      <b>Выполнить до:</b> {{ task_deadline|datetime }}\n'
            '\n'
            '⭐️ <b>Награда:</b> {{task_reward_points|plural(["балл", "балла", "баллов"])}}\n'
            '\n'
            '{% if people_completed_task_amount != 0 %}'
            '👥 Уже <b>{{ people_completed_task_amount|plural(["человек", "человека", "человек"]) }}</b> выполнили это задание!'
            '{% endif %}'
        ),
        Row(
            Button(
                Const('⬅️'),
                id='GOVNOCODE_PREV_TASK',
                on_click=govnocode_pagination,
                when=F['prev_page'].is_not(None),
            ),
            Button(
                Const('➡️'),
                id='GOVNOCODE_NEXT_TASK',
                on_click=govnocode_pagination,
                when=F['next_page'].is_not(None),
            )
        ),
        Row(
            Button(
                Const('✅ Выполнить'),
                id='complete_activity_task',
                on_click=on_complete_activity_task_click,
            ),
            Next(Const('❌ Отказаться'), id='decline_activity_task'),
        ),
        Button(
            Const('⬅️ Назад'),
            id='back_to_activity',
            on_click=on_back_to_activity_click,
        ),
        state=states.ActivityTask.MAIN
    ),
    Window(
        Jinja(
            '❌ <b>Отказ от задания</b>\n'
            '\n'
            '🤔 Ты точно хочешь отказаться от задания «{{task_name}}»? '
            'Ты не получишь баллов и понизишься в рейтинге. Напоминаю, призовой фонд активности {{activity_fund|money}}!'
        ),
        Row(
            Back(Const('⬅️ Назад')),
            Button(
                Const('✅ Да, я отказываюсь'),
                id='cancel_activity_task',
                on_click=on_cancel_task_click,
            ),
        ),
        getter=activity_getter,
        state=states.ActivityTask.DECLINE
    ),
    Window(
        Const(
            '❌ <b>Отказ от задания</b>\n'
            '\n'
            'Задание пропущено. Ожидай следующего задания.\n'
            'Если отказался от задания по ошибке — пиши @ambienthugg'
        ),
        Cancel(Const('✅ Готово')),
        state=states.ActivityTask.SURE_DECLINE
    ),
    getter=(activity_task_getter, pagination_getter),
    on_start=on_fucking_start_activity,
)
