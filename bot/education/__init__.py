__all__ = ['register_education_handler', 'Words']

from bot.education.classes import Words

from bot.education.learn import Level, Test
from bot.education.learn import testing, learning, result

from bot.education.repeat import resut_repeat
from bot.education.repeat import Repeat

from aiogram import Router
from aiogram import F


def register_education_handler(router: Router):
    router.message.register(learning, Level.level)
    router.message.register(result, Test.answer)

    router.message.register(resut_repeat, Repeat.answer)
