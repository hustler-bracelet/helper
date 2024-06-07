import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.dialogs import states


async def activities_list_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'activities': [
            ('мешок денег', 'Сезон крипты', 0),  # emoji, name, id
            ('солнышко', 'Летний хасл жесть', 1)
        ]
    }


async def on_choose_activity(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: int
):
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
)
