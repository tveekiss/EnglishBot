__all__ = ['register_education_handler', 'starting', 'Words', 'statistics', 'repeat']

from bot.education.classes import Words

from bot.education.learn import Level, Test
from bot.education.learn import starting, testing, learning, result

from bot.education.repeat import resut_repeat, repeat
from bot.education.repeat import Repeat

from bot.education.statistics import statistics

from aiogram import Router


def register_education_handler(router: Router):
    router.message.register(learning, Level.level)
    router.message.register(result, Test.answer)

    router.message.register(resut_repeat, Repeat.answer)
