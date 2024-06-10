import datetime
import random

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Start, Next, Back
from aiogram_dialog.widgets.text import Format, Jinja, Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.bot.dialogs.activity import activity_getter, activity_task_getter


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
                Const('✅ Выполнить'),
                id='complete_activity_task',
                on_click=on_complete_activity_task_click,
            ),
            Next(Const('❌ Отказаться'), id='decline_activity_task'),
        ),
        Cancel(Const('⬅️ Назад')),
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
            Next(Const('✅ Да, я отказываюсь'))
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
    getter=activity_task_getter
)
