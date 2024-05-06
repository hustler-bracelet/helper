import datetime
from typing import Any, Callable

from aiogram import types, html
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.input.text import TypeFactory, OnSuccess, OnError, ManagedTextInput
from aiogram_dialog.widgets.kbd.button import Button
from aiogram_dialog.widgets.kbd.calendar_kbd import OnDateSelected
from aiogram_dialog.widgets.kbd.state import EventProcessorButton
from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor, ensure_event_processor
from simpleeval import SimpleEval


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


class NumberInput(TextInput):
    def __init__(
            self,
            id: str = '__number_input__',
            type_factory: TypeFactory = str,
            on_success: OnSuccess | WidgetEventProcessor | None = None,
            filter: Callable[[float], Any] | None = None,
            on_error: OnError | WidgetEventProcessor | None = None,
    ):
        super().__init__(
            id=id,
            type_factory=self._type_factory,
            on_success=on_success,
            on_error=on_error or self._on_error,
            filter=filter
        )

        self.user_type_factory = type_factory

        self.evaluator = SimpleEval()

    def _type_factory(self, text: str) -> float | Any:
        amount = text.lower()

        replace_mapping = {
            ' ': '',
            ',': '.',
            '^': '**',
            ':': '/'
        }
        for old, new in replace_mapping.items():
            amount = amount.replace(old, new)

        try:
            amount = self.evaluator.eval(amount)
        except BaseException:
            raise ValueError('Кажется, ты ввёл неправильную формулу')

        if self.user_type_factory:
            amount = self.user_type_factory(amount)

        return amount

    async def _on_error(
            self,
            message: types.Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            error: ValueError,
    ):
        await message.answer('\n'.join([*map(html.quote, error.args), 'Попробуй ещё раз']))
