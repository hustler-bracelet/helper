import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.button import Button
from aiogram_dialog.widgets.kbd.calendar_kbd import OnDateSelected
from aiogram_dialog.widgets.kbd.state import EventProcessorButton
from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor, ensure_event_processor


class Today(EventProcessorButton):
    def __init__(
            self,
            calendar_on_click: OnDateSelected | WidgetEventProcessor,
            text: Text = Const('Сегодня'),
            id: str = "__today__",
            result: Any = None,
            when: WhenCondition = None,
    ):
        super().__init__(
            text=text, on_click=self._on_click,
            id=id, when=when,
        )
        self.text = text
        self.result = result
        self.calendar_on_click = ensure_event_processor(calendar_on_click)

    async def _on_click(
            self,
            callback: CallbackQuery,
            button: Button,
            manager: DialogManager,
    ):
        return await self.calendar_on_click.process_event(
            manager.event,
            button,
            manager,
            selected_date=datetime.date.today()
        )
