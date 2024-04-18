import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

import config
from .handlers import router


async def main():
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(config.TG_BOT_TOKEN, parse_mode=ParseMode.HTML)

    await bot.set_my_commands(
        [
            types.BotCommand(command='start', description='Перезапуск бота'),
            types.BotCommand(command='cancel', description='Выход из диалога')
        ]
    )

    dp = Dispatcher()
    dp.include_router(router)

    # loop_task: Optional[Task] = None
    #
    # async def on_startup():
    #     nonlocal loop_task
    #     loop_task = asyncio.create_task(loop(bot))
    #
    # def on_shutdown():
    #     nonlocal loop_task
    #     loop_task.cancel()
    #
    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
