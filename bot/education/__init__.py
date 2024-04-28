__all__ = ['register_education_handlers', 'starting', 'repeat_new', 'repeat_old', 'statistic', 'old_statistics']

from bot.education.learn import starting, introduction, Test, result
from aiogram import Router
from bot.education.repeat import repeat_new, result_repeat, Repeat
from bot.education.repeat_old import repeat_old, RepeatOld, result_old
from bot.education.statistic import statistic, old_statistics


def register_education_handlers(router: Router):
    router.message.register(introduction, Test.level)
    router.message.register(result, Test.answer)

    router.message.register(result_repeat, Repeat.answer)
    router.message.register(result_old, RepeatOld.answer)
