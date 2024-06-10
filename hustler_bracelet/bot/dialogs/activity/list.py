import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states

from hustler_bracelet.client import ActivityAPIClient
from hustler_bracelet.client.schemas import ActivityDataResponse


client = ActivityAPIClient()


async def on_start_list_activity(start_data: dict, dialog_manager: DialogManager):
    activities = await client.get_activities(is_active=True)

    dialog_manager.dialog_data.update({
        'activities': activities
    })


async def activities_list_getter(dialog_manager: DialogManager, **kwargs):
    activities: list[ActivityDataResponse] = dialog_manager.dialog_data['activities']

    return {
        'activities': [
            (activity.emoji, activity.name, activity.id)
            for activity in activities
        ]
    }


async def on_choose_activity(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: int
):
    activity_id = item_id
    user_id = callback.from_user.id

    result = await client.activity_status(activity_id, user_id)

    if not result.already_joined:
        if not result.is_running:
            await callback.answer('Данная активность уже закончилась.', show_alert=True)
            return

        elif result.occupied_places == result.total_places:
            await callback.answer('Данная активность переполнена.', show_alert=True)
            return

        elif result.can_join is False:
            await callback.answer('Вы покинули данную активность.', show_alert=True)
            return

    await manager.start(
        states.Activity.MAIN,
        {'activity_id': item_id}  # dialog_manager.start_data['activity_id']
    )


activities_list_dialog = Dialog(
    Window(
        Const('В какой активной активности будешь активничать?'),
        ScrollingGroup(
            Select(
                Format('{item[0]} {item[1]}'),
                id='slct_activity',
                item_id_getter=operator.itemgetter(2),
                items='activities',
                on_click=on_choose_activity
            ),
            id="scrl_activities",
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Cancel(Const('❌ Отмена')),
        state=states.ActivitiesList.MAIN,
        getter=activities_list_getter
    ),
    on_start=on_start_list_activity,
)
