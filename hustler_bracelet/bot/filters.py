from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter

import config


async def check_sub(bot: Bot, channel_id: int, user_id: int) -> bool:
    try:
        user = await bot.get_chat_member(channel_id, user_id)
        return user.status != "left"
    except TelegramBadRequest as e:
        print('Error on access checking', e)
        return False


class SubChecker(BaseFilter):
    async def __call__(self, event: types.Message | types.CallbackQuery, bot: Bot) -> bool:
        sub = await check_sub(bot, config.BRACELET_CHANNEL_ID, event.from_user.id)

        if sub:
            return True

        await bot.send_message(
            event.from_user.id,
            '❌ <b>Бот доступен только для участников HUSTLER BRACELET!</b>\n'
            '\n'
            'Вступить - @ambienthugg / @hustler_ambi\n'
            'По техническим вопросам - @d_nsdkin / @farel106'
        )
        return False


class AdminFilter(BaseFilter):
    async def __call__(self, callback: types.CallbackQuery | types.Message, bot: Bot) -> bool:
        return callback.from_user.id == 1702948486
