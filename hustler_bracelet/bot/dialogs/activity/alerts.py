
from aiogram import Router, types, F

from hustler_bracelet.bot.dialogs import states
from hustler_bracelet.client import ActivityAPIClient
from aiogram_dialog import Dialog, DialogManager, StartMode


activity_client = ActivityAPIClient()


alert_router = Router()


@alert_router.message(F.text.startswith('open_activity_task'))
async def open_activity_task(callback: types.CallbackQuery, dialog_manager: DialogManager):
    activity_id = int(callback.data.split(':')[-1])

    status = await activity_client.activity_status(
        activity_id=activity_id,
        user_id=dialog_manager.event.from_user.id,
    )

    if not status.already_joined:
        if not status.is_running:
            await callback.answer('Данная активность уже закончилась.', show_alert=True)
            return

        elif status.occupied_places == status.total_places:
            await callback.answer('Данная активность переполнена.', show_alert=True)
            return

        elif status.can_join is False:
            await callback.answer('Вы покинули данную активность.', show_alert=True)
            return

    activity_summary = await activity_client.get_activity_user_summary(
        user_id=dialog_manager.event.from_user.id,
        activity_id=activity_id,
    )

    await dialog_manager.start(
        states.ActivityTask.MAIN,
        data={
            'activity_summary': activity_summary,
        }
    )
