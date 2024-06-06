from aiogram import types, F
from aiogram_album import AlbumMessage
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states


async def on_done_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    await manager.done()


async def media_group_handler(
        message: AlbumMessage,
        message_input: MessageInput,
        manager: DialogManager,
):
    messages_ids = [*map(lambda msg: msg.message_id, message.messages)]  # Это у каждого сообщения своё
    media_group_id = message.media_group_id  # Это общая хуйня

    # await message.bot.copy_messages(  # Это чисто для меня, не обращай внимания
    #     message.from_user.id,  # В какой чат слать (амби)
    #     message.from_user.id,  # Из какого чата копируем сообщения
    #     messages_ids
    # )
    await manager.next()


async def message_handler(
        message: types.Message,
        message_input: MessageInput,
        manager: DialogManager,
):
    # Это альтернатива mediagroup_handler. Нужно что-то взять вместо media_group_id, чтобы поведение было консистентным
    # Судя по разнице в длине айдишников сообщений и медиагрупп, коллизий между ними не бывает, так что можно просто взять message_id
    message_id = message.message_id
    # media_group_id = message_id ???
    await manager.next()


complete_task_dialog = Dialog(
    Window(
        Const(
            '✅ <b>Выполнение задания</b>\n'
            '\n'
            'Чтобы подтвердить, что ты выполнил задание, отправь пруфы (скрины, либо что-то другое, указанное в описании задания).\n'
            '\n'
            'Администраторы рассмотрят твоё подтверждение и засчитают задание выполненным, а ты получишь баллы и поднимешься в топе.'
        ),
        MessageInput(
            media_group_handler,
            filter=F.media_group_id
        ),
        MessageInput(
            message_handler
        ),
        state=states.ActivityTaskCompletion.MAIN
    ),
    Window(
        Const(
            '✅ <b>Выполнение задания</b>\n'
            '\n'
            'Задание отправлено на проверку.\n'
            'Если отправил не те скриншоты — пиши @ambienthugg'
        ),
        Cancel(Const('✅ Готово'), on_click=on_done_click),
        state=states.ActivityTaskCompletion.FINAL
    )
)
