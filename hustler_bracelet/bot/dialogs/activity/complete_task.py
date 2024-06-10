from aiogram import types, F
from aiogram_album import AlbumMessage
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.client import ProofsAPIClient
from hustler_bracelet.client.schemas import ProofCreate, ProofResponse, ActivitySummaryResponse


proofs_client = ProofsAPIClient()


async def on_dialog_start(start_data, manager: DialogManager):
    manager.dialog_data.update({
        'activity_summary': start_data.get('activity_summary'),
    })


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
    activity: ActivitySummaryResponse = manager.dialog_data.get('activity_summary')
    photo_ids = [
        message.photo[-1].file_id
        for message in message.messages
        if message.photo
    ]
    caption = message.caption

    await proofs_client.create_proof(ProofCreate(
        user_id=message.from_user.id,
        task_id=activity.niche.task.id,
        photo_ids=photo_ids,
        caption=caption
    ))

    await manager.next()


async def message_handler(
        message: types.Message,
        message_input: MessageInput,
        manager: DialogManager,
):
    caption = message.text or message.caption

    photo_ids = [message.photo[-1].file_id] if message.photo else []

    await proofs_client.create_proof(ProofCreate(
        user_id=message.from_user.id,
        task_id=manager.dialog_data.get('activity_summary').niche.task.id,
        photo_ids=photo_ids,
        caption=caption
    ))

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
    ),
    on_start=on_dialog_start,
)
