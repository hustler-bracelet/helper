# -*- coding: utf-8 -*-
import datetime
import operator
import random
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Back, Cancel, Next, ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Format, Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.client.schemas.activities import ActivitySummaryResponse
from hustler_bracelet.managers import FinanceManager

from hustler_bracelet.client import ActivityAPIClient, NichesAPIClient, ActivityTasksAPIClient
from hustler_bracelet.client.schemas import ActivityDataResponse, NicheDataResponse, ActivitySummaryResponse, ActivityTaskStatus


activity_client = ActivityAPIClient()
niche_client = NichesAPIClient()
tasks_client = ActivityTasksAPIClient()


async def on_start_activity_dialog(start_data: dict, manager: DialogManager):
    user_id = manager.event.from_user.id
    activity_id = start_data['activity_id']

    # NOTE: получаем информацию о активности для пользователя
    activity_summary: ActivitySummaryResponse | None = await activity_client.get_activity_user_summary(user_id, activity_id)

    # отправляем на этап выбора ниши, если она не установлена
    if not activity_summary:
        # NOTE: получаем общую информациюю о активности
        activity = await activity_client.get_current_activity()
        await manager.start(states.ActivityOnboarding.MAIN, data={'activity': activity})
        return

    manager.dialog_data.update({
        'activity_summary': activity_summary,
    })


async def on_process_result(
        start_data: dict,
        result_data: dict,
        dialog_manager: DialogManager
):
    if result_data and result_data.get('show_task', True):
        await dialog_manager.start(states.ActivityTask.MAIN)
        return


async def on_current_task_click(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data or dialog_manager.start_data
    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    if not activity_summary.niche.task:
        await callback.answer('Нет активных задач', show_alert=True)
        return

    result = await tasks_client.get_status_for_user(
        user_id=dialog_manager.event.from_user.id,
        task_id=activity_summary.niche.task.id
    )

    if result.already_done:
        await callback.answer('Вы уже выполнили эту задачу', show_alert=True)
        return

    if not result.can_do_task:
        await callback.answer('Вы не можете выполнять эту задачу', show_alert=True)
        return

    await dialog_manager.start(
        states.ActivityTask.MAIN, 
        data={
            'activity_summary': dialog_manager.dialog_data['activity_summary'],
        }
    )


async def top_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    return {
        "points": activity_summary.user_leaderboard_data.points if activity_summary.user_leaderboard_data else 0,
        "current_top_position": activity_summary.user_leaderboard_data.position if activity_summary.user_leaderboard_data else 0
    }


async def activity_task_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    return {
        'task_name': activity_summary.niche.task.name if activity_summary.niche.task else '-',
        'task_emoji': '',
        'task_caption': activity_summary.niche.task.description if activity_summary.niche.task else '-',
        'task_sent_at': activity_summary.niche.task.added_on if activity_summary.niche.task else None,
        'task_deadline': activity_summary.niche.task.deadline if activity_summary.niche.task else None,
        'task_reward_points': activity_summary.niche.task.points if activity_summary.niche.task else 0,  # TODO: Уточнить, только ли баллы могут быть в награде
        'people_completed_task_amount': 0,  # TODO: добавить в саммари блять 
    }


async def activity_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    return {
        "activity_name": f"{activity_summary.emoji} {activity_summary.name}",
        "activity_description": activity_summary.description,
        "activity_launched_at": activity_summary.started_on,
        "activity_deadline": activity_summary.deadline,
        "activity_fund": activity_summary.fund,
        "activity_places": activity_summary.total_places,
        "current_niche": f"{activity_summary.niche.emoji} {activity_summary.niche.name}",
        "current_points_balance": activity_summary.user_leaderboard_data.points if activity_summary.user_leaderboard_data else 0,
        "current_top_position": activity_summary.user_leaderboard_data.position if activity_summary.user_leaderboard_data else 0,
        "task_name": {activity_summary.niche.task.name if activity_summary.niche.task else '-'},
        "task_reward_points": {activity_summary.niche.task.points if activity_summary.niche.task else 0},
        "task_deadline": {activity_summary.niche.task.deadline  if activity_summary.niche.task else None},
    }


async def activity_top_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    if not activity_summary.leaderboard_data:
        return []

    activity_summary.leaderboard_data = sorted(
        activity_summary.leaderboard_data, 
        key=lambda x: x.points, 
        reverse=True
    )

    return {
        'top': [
            (
                data.user.telegram_name, 
                data.position, 
                data.points, 
                data.user.telegram_id == dialog_manager.event.from_user.id,
            )
            for data in activity_summary.leaderboard_data
        ]
    }


async def on_exit_activity_click(
    callback,
    button,
    manager: DialogManager,
):
    await manager.start(
        states.ActivityQuit.MAIN,
        data={
            'activity_summary': manager.dialog_data['activity_summary'],
        }
    )


async def on_back_to_main_click(
    callback,
    button,
    manager: DialogManager
):
    await manager.start(states.Main.MAIN)


activity_dialog = Dialog(
    Window(
        Jinja(
            "<b>{{activity_name}}</b>\n"
            "\n"
            "{{activity_description}}\n"
            "\n"
            "🗓 <b>Начало:</b> {{activity_launched_at|datetime}}\n"
            "      <b>Окончание:</b> {{activity_deadline|datetime}}\n"
            "🤑 <b>Призовой фонд:</b> {{activity_fund|money}}\n"
            "      <b>Мест:</b> {{activity_places}}\n"
            "\n"
            "💼 <b>Твоя ниша:</b> {{current_niche}}\n"
            "🪙 <b>Баллов заработано:</b> {{points|number}} (в топе: на {{current_top_position|number}} месте)\n"  # TODO: мб стоит предусмотреть округление current_top_position
            "\n"
            "👉 <b>Текущее задание:</b> {{task_name}} ({{task_reward_points|plural(['балл', 'балла', 'баллов'])}})\n"
            "🕐 <b>Выполнить до:</b> {{task_deadline|datetime}}"
        ),
        Button(
            Const('✅ Текущее задание'),
            id='current_task_btn',
            on_click=on_current_task_click,
        ),
        Next(
            Const('🏆 Топ участников'),
            id='activity_top_btn',
        ),
        # Button(
        #     Const('❌ Выйти с активности (сдаться)'),
        #     id='activity_quit_btn',
        #     on_click=on_exit_activity_click,
        # ),
        Button(
            Const('⬅️ Назад'),
            id='back_to_main_btn',
            on_click=on_back_to_main_click,
        ),
        state=states.Activity.MAIN,
        getter=(activity_getter, activity_task_getter, top_getter),
    ),
    Window(
        Jinja(
            '🏆 <b>Топ участников</b>\n'
            '\n'
            '{% for i in range(top|length) %}\n'
            '    {% set item = top[i] %}\n'
            '    {% if i == 0 %}\n'
            '1. <b>{% if item[3] %}👉🏻 {% endif %}🥇 {{ item[0] }}</b> — {{ item[1] }} баллов — <b>{{ item[2] }}₽{% if item[3] %} 👈🏻{% endif %}</b>\n'
            '    {% elif i == 1 %}\n'
            '2. <b>{% if item[3] %}👉🏻 {% endif %}🥈 {{ item[0] }}</b> — {{ item[1] }} баллов — <b>{{ item[2] }}₽{% if item[3] %} 👈🏻{% endif %}</b>\n'
            '    {% elif i == 2 %}\n'
            '3. <b>{% if item[3] %}👉🏻 {% endif %}🥉 {{ item[0] }}</b> — {{ item[1] }} баллов — <b>{{ item[2] }}₽{% if item[3] %} 👈🏻{% endif %}</b>\n'
            '    {% else %}\n'
            '{{ i+1 }}. <b>{% if item[3] %}👉🏻 {% endif %}{{ item[0] }}</b> — {{ item[1] }} баллов — <b>{{ item[2] }}₽{% if item[3] %} 👈🏻{% endif %}</b>\n'
            '    {% endif %}\n'
            '{% endfor %}'
            ),
        Back(Const('⬅️ Назад')),
        state=states.Activity.TOP,
        getter=activity_top_getter,
    ),
    on_start=on_start_activity_dialog,
    on_process_result=on_process_result,
)
