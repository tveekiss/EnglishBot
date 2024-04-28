__all__ = ['register_handlers', 'start_register']

from bot.handlers.register import start_register, Register, register_name
from aiogram import Router, F

from bot.education import starting, repeat_old, repeat_new, statistic, old_statistics
from bot.handlers.repeat import repeat_choice


def register_handlers(router: Router):
    router.message.register(register_name, Register.username, flags={'username': 'username'})

    router.message.register(starting, F.text == '📚 Учить слова')
    router.message.register(repeat_choice, F.text == '🧠 Повторить')

    router.message.register(repeat_old, F.text == '🗓️ Повторить старые слова')
    router.message.register(repeat_new, F.text == '🧠 Закрепить новые слова')

    router.message.register(statistic, F.text == '✍️ Статистика')
    router.message.register(old_statistics, F.text == '📋 Посмотреть базу выученных слов')

