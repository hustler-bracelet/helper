# -*- coding: utf-8 -*-

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Back
from aiogram_dialog.widgets.text import Format, Const

from hustler_bracelet.bot.dialogs import states

ACTIVITY_DESCRIPTION = """Ну что, хаслеры, время пампить, дампить, хуямпить, МММ’ить, и регулировать стаканы!
Выбирай свою нишу и вперёд жарить стейкинги!"""


async def top_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "points": "20",
        "current_top_position": "18"
    }


async def current_task_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "current_task_name": "Слить все монеты",
        "current_task_description": "Этот броуски больше не любит Пашу Дурова",
        "current_task_points": "5",
        "current_task_sent_at": "2 июня (16:33 МСК)",
        "current_task_deadline": "3 июня (23:59 МСК)",
        "current_task_completions_amount": "2"
    }


async def activity_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "activity_name": "💰 Сезон крипты",
        "activity_description": ACTIVITY_DESCRIPTION,
        "activity_launched_at": "1 июня 2024 (23:59 МСК)",
        "activity_deadline": "7 июня 2024 (23:59 МСК)",
        "activity_fund": "100 000₽",
        "activity_places": "20",
        "current_niche": "TON staker",
        "current_points_balance": "18",
    }


activity_dialog = Dialog(
    Window(
        Format(
            """{activity_name}

{activity_description}

🗓 Начало: {activity_launched_at}
      Окончание: {activity_deadline}
🤑 Призовой фонд: {activity_fund}
      Мест: {activity_places}

💼 Твоя ниша: {current_niche}
🪙 Баллов заработано: {points} (в топе: на {current_top_position} месте)

👉 Текущее задание: {current_task_name} ({current_task_points} баллов)
🕐 Выполнить до: {current_task_deadline}"""
        ),
        Start(
            Const('✅ Текущее задание'),
            id='current_task_btn',
            state=states.ActivityTask.MAIN
        ),
        Start(
            Const('🏆 Топ участников'),
            id='activity_top_btn',
            state=states.Activity.TOP
        ),
        Start(
            Const('❌ Выйти с активности (сдаться)'),
            id='activity_quit_btn',
            state=states.ActivityQuit.MAIN
        ),
        Back(Const('⬅️ Назад')),
        state=states.Activity.MAIN
    ),
    getter=(activity_getter, current_task_getter, top_getter),
)

