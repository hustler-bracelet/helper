from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, Next, Button
from aiogram_dialog.widgets.text import Jinja, Const

from hustler_bracelet.bot.dialogs import states

from hustler_bracelet.client import ActivityAPIClient
from hustler_bracelet.client.schemas import ActivitySummaryResponse


client = ActivityAPIClient()


async def on_start_dialog(
    start_data: dict, manager: DialogManager
):
    activity_summary: ActivitySummaryResponse = start_data.get('activity_summary')

    manager.dialog_data.update(
        {
            'activity_summary': activity_summary
        }
    )


async def activity_quit_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data or dialog_manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    if not activity_summary.leaderboard_data:
        return {
            'place_in_top': 0,
            'possible_reward': 0,
        }

    for data in activity_summary.leaderboard_data:
        if data.user.telegram_id == dialog_manager.event.from_user.id:
            return {
                'place_in_top': data.position,
                'possible_reward': data.earn,
            }

    return {
        'place_in_top': 0,
        'possible_reward': 0,
    }


async def on_exit_click(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager
):
    data = manager.dialog_data or manager.start_data

    activity_summary: ActivitySummaryResponse = data.get('activity_summary')

    await client.leave_activity(
        manager.event.from_user.id,
        activity_id=activity_summary.id,
    )


async def on_done_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    await manager.done()


activity_quit_dialog = Dialog(
    Window(
        Jinja(
            '❌ <b>Выход из активности</b>\n'
            '\n'
            '🤔 Ты точно хочешь выйти из текущей активности?\n'
            'Ты сейчас на {{place_in_top|number}}-ом месте и можешь получить <b>{{possible_reward|money}}</b>!\n'
            'Слабовато как-то...'
        ),
        Row(
            Cancel(Const('⬅️ Назад')),
            Next(Const('✅ Да, я хочу выйти'), on_click=on_exit_click)
        ),
        state=states.ActivityQuit.MAIN,
        getter=activity_quit_getter
    ),
    Window(
        Const(
            '❌ <b>Выход из активности</b>\n'
            '\n'
            'Жаль. Ожидай следующей активности.\n'
            'Если вышел по ошибке — пиши @ambienthugg'
        ),
        Cancel(Const('✅ Готово'), on_click=on_done_click),
        state=states.ActivityQuit.FINAL
    ),
    on_start=on_start_dialog,
)
