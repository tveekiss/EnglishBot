__all__ = ['register_user_handlers']


from aiogram import Router
from aiogram import F

from bot.handlers.register import start_register, register_name, Register
from bot.education import starting
from bot.education import repeat
from bot.education import statistics


def register_user_handlers(router: Router):
    # Регистрация пользователя
    router.message.register(start_register, F.text == 'Начать')
    router.message.register(register_name, Register.username)
    # Выбор действия
    router.message.register(starting, F.text == 'Учить слова')
    router.message.register(repeat, F.text == 'Повторить')
    router.message.register(statistics, F.text == 'Статистика')
