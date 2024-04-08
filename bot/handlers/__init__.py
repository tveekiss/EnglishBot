__all__ = ['register_user_handlers']


from aiogram import Router
from aiogram import F

from bot.handlers.register import start_register, register_name, Register
from bot.education import starting

from bot.education import repeat
from bot.education import repeat_old

from bot.education import statistics, old_statistics
from bot.handlers.repeat import repeat_choice

from bot.commands import start_command


def register_user_handlers(router: Router):
    # Регистрация пользователя
    router.message.register(start_register, F.text == 'Начать')
    router.message.register(register_name, Register.username)
    # Выбор действия
    router.message.register(starting, F.text == 'Учить слова')
    router.message.register(repeat_choice, F.text == 'Повторить')

    router.message.register(statistics, F.text == 'Статистика')
    router.message.register(old_statistics, F.text == 'Посмотреть базу выученных слов')
    # Выбор повтора
    router.message.register(repeat_old, F.text == 'Повторить старые слова')
    router.message.register(repeat, F.text == 'Повторить новые слова')
    # Вернуться на главную страницу
    router.message.register(start_command, F.text == 'Назад')
