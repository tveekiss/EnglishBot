from aiogram import Bot, Dispatcher
import os
import asyncio
import logging

from commands import register_user_commands, commands_list
from bot.handlers import register_handlers
from bot.education import register_education_handlers
from bot.database.db import Base, engine
from bot.middlewaries import RegisterCheckMiddleware

dp = Dispatcher()
bot = Bot(token='6961090140:AAFtEO8OPGu_z-wOn1-FnkNbto_UgKr9WUw')


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.message.middleware(RegisterCheckMiddleware())

    register_user_commands(dp)
    register_handlers(dp)
    register_education_handlers(dp)
    await commands_list.set_commands_list(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
