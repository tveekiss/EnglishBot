from aiogram import Bot, Dispatcher
import os
import asyncio
import logging

from commands import register_user_commands, commands_list
from handlers import register_user_handlers

dp = Dispatcher()
bot = Bot(token=os.getenv('token'))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    register_user_commands(dp)
    register_user_handlers(dp)
    await commands_list.set_commands_list(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
