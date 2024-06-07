# -*- coding: utf-8 -*-
import datetime
import operator
import random
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Back, Cancel, Next, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Const, Jinja

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.managers import FinanceManager


async def on_start_activity_dialog(start_data: dict, manager: DialogManager):
    if True:  # random.randint(0, 1):  # Если ниша не выбрана
        await manager.start(states.ActivityOnboarding.MAIN)
        return


async def on_process_result(
        start_data: dict,
        result_data: dict,
        dialog_manager: DialogManager
):
    if result_data and result_data.get('show_task', True):
        await dialog_manager.start(states.ActivityTask.MAIN)
        return


async def top_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "points": 20,
        "current_top_position": 18
    }


async def activity_task_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'task_name': 'Слить все токены',
        'task_emoji': '⚡️',
        'task_caption': 'Этот броуски больше не любит Пашу Дурова',
        'task_sent_at': datetime.datetime.now(),
        'task_deadline': datetime.datetime.now() + datetime.timedelta(days=10),
        'task_reward_points': 4,  # TODO: Уточнить, только ли баллы могут быть в награде
        'people_completed_task_amount': 22 * random.randint(0, 1),
    }


async def activity_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "activity_name": "💰 Сезон крипты",
        "activity_description": "Ну что, хаслеры, время пампить, дампить, хуямпить, МММ’ить, и регулировать стаканы!\n"
                                "Выбирай свою нишу и вперёд жарить стейкинги!",
        "activity_launched_at": datetime.datetime.now(),
        "activity_deadline": datetime.datetime.now() + datetime.timedelta(days=10),
        "activity_fund": 100_000,
        "activity_places": 20,
        "current_niche": "TON staker",
        "current_points_balance": 18,
    }


async def activity_top_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'top': [
            ('Дмитрий', 20, 20233.27, False),
            ('Farel', 20, 16186.62, False),
            ('Игорь', 18, 12949, False),
            ('ambienthugg', 18, 10359.44, True),
            ('Женьчик', 18, 8287.55, False),
            ('Работает Артур', 18, 6630.04, False),
            ('Vladimir', 16, 5304.03, False),
            ('CHVS', 16, 4243.23, False),
            ('Honex', 16, 3394.58, False),
            ('Kirill Usenko', 14, 2715.66, False),
            ('Jesus', 12, 2172.53, False),
            ('Споки | 1k ROI', 10, 1738.02, False),
            ('Tony', 10, 1390.42, False),
            ('Влад', 8, 1112.34, False),
            ('Сергей', 8, 889.87, False),
            ('Kartright', 6, 711.90, False),
            ('Jesus', 4, 569.52, False),
            ('Yankee', 4, 455.61, False),
            ('Igor', 2, 364.49, False),
            ('Un/tilt/ed', 2, 291.59, False)
        ]
    }


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
        Start(
            Const('✅ Текущее задание'),
            id='current_task_btn',
            state=states.ActivityTask.MAIN
        ),
        Next(
            Const('🏆 Топ участников'),
            id='activity_top_btn'
        ),
        Start(
            Const('❌ Выйти с активности (сдаться)'),
            id='activity_quit_btn',
            state=states.ActivityQuit.MAIN
        ),
        Cancel(Const('⬅️ Назад')),
        state=states.Activity.MAIN,
        getter=(activity_getter, activity_task_getter, top_getter)
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
    on_process_result=on_process_result
)
