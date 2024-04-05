__all__ = ['register_user_handlers']


from aiogram import Router
from aiogram import F

from bot.handlers.register import start_register, register_name, Register


def register_user_handlers(router: Router):
    # Регистрация пользователя
    router.message.register(start_register, F.text == 'Начать')
    router.message.register(register_name, Register.username)

    # Callbacks