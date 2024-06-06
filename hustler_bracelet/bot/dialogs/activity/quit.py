from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, Next, Button
from aiogram_dialog.widgets.text import Jinja, Const

from hustler_bracelet.bot.dialogs import states


async def activity_quit_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'place_in_top': 4,
        'possible_reward': 10_359.44,
    }


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
            Next(Const('✅ Да, я хочу выйти'))
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
    )
)
