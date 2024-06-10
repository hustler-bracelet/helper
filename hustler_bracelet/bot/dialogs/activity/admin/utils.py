
from aiogram import types


class SimplePagination:
    def __init__(
        self, 
        items: list, 
        start_callback: str,
        current_page: int = 0,
    ):
        self._items = items
        self._current_page = current_page
        self.start_callback = start_callback

    def load_from_callback_data(self, callback_data: str):
        page = int(callback_data.split(':')[-1])
        self._current_page = page
        return self

    def get_current_data(self):
        return self._items[self._current_page]

    def get_pagination_buttons(self):
        buttons = []

        if self._current_page > 0:
            buttons.append(types.InlineKeyboardButton(text='⬅️', callback_data=f'{self.start_callback}:{self._current_page - 1}'))

        if self._current_page < len(self._items) - 1:
            buttons.append(types.InlineKeyboardButton(text='➡️', callback_data=f'{self.start_callback}:{self._current_page + 1}'))

        return buttons
