from aiogram import types


def get_main_menu_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Финансы', callback_data='finance_menu'),
                types.InlineKeyboardButton(text='Планирование', callback_data='tasks_menu'),
                types.InlineKeyboardButton(text='Спорт', callback_data='sport_menu'),
            ]
        ]
    )
