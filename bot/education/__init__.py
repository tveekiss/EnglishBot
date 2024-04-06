__all__ = ['register_education_handler']

from bot.education.learn import Level, Test
from bot.education.learn import testing, learning, result

from aiogram import Router
from aiogram import F


def register_education_handler(router: Router):
    router.message.register(learning, Level.level)
    router.message.register(result, Test.answer)

