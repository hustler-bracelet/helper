from datetime import date

from aiogram import types
from aiogram.types import ForceReply
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Calendar, ManagedCalendar, Button, ScrollingGroup, Back, Start
)
from aiogram_dialog.widgets.text import Const, Format

from hustler_bracelet.bot.bot_dialogs import states
from hustler_bracelet.bot.bot_dialogs.common import MAIN_MENU_BUTTON
from hustler_bracelet.bot.callbacks import CategoryForNewEventCallback
from hustler_bracelet.bot.utils import get_finance_event_type_name, finance_event_name_getter
from hustler_bracelet.enums import FinanceEventType


async def on_date_clicked(
        callback: ChatEvent,
        widget: ManagedCalendar | None,
        manager: DialogManager,
        selected_date: date,
):
    await callback.answer(str(selected_date))
    manager.dialog_data['event_date'] = selected_date
    await manager.next()


async def on_today_clicked(
        callback: ChatEvent,
        button: Button,
        manager: DialogManager,
):
    return await on_date_clicked(
        callback=callback,
        widget=None,
        manager=manager,
        selected_date=date.today()
    )


async def on_add_category_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.start(
        state=states.AddFinanceCategory.GET_NAME,  # Скипаем первый этап, т.к. ответ на первый вопрос (тип категории) уже известен
        data={'cat_type': manager.start_data['event_type']}
    )


async def on_choose_category_click(
        callback: types.CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await callback.answer()
    category_id = CategoryForNewEventCallback.unpack(value=callback.data).category_id
    event_date = manager.dialog_data['event_date']

    await callback.message.answer(f'Ты выбрал категорию {category_id} эмм чел типа окок создам я твою хуйню')


add_event_dialog = Dialog(
    Window(
        Format('Налоговая хочет знать точную дату твоих {finance_event_name}'),
        Calendar(
            id='fin_calendar',
            on_click=on_date_clicked,
        ),
        Button(
            id='fin_today',
            text=Const('Сегодня'),
            on_click=on_today_clicked,
        ),
        MAIN_MENU_BUTTON,

        state=states.AddFinanceEvent.MAIN,
    ),
    Window(
        Format('Налоговая хочет знать категорию твоих {finance_event_name}'),
        ScrollingGroup(
            Button(text=Const('Банки'), id=CategoryForNewEventCallback(category_id=0).pack(), on_click=on_choose_category_click),
            Button(text=Const('Хуянки'), id=CategoryForNewEventCallback(category_id=1).pack(), on_click=on_choose_category_click),
            id="fin_category",
            width=1,
            height=6,
            hide_on_single_page=True
        ),
        Button(text=Const('➕ Добавить категорию'), id='add_fin_category', on_click=on_add_category_click),
        Back(),
        state=states.AddFinanceEvent.CHOOSE_CATEGORY,
    ),
    getter=finance_event_name_getter,
)
