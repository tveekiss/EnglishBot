__all__ = ['register_user_commands', 'commands_list', 'start_command']

from aiogram import Router, F
from aiogram.filters import Command

from bot.commands.start import start_command
from bot.commands.help import (
    help_command,
    call_repeat, call_repeat_old, call_repeat_choice,
    call_statistics, call_statistics_list,
    call_learn, call_back
)
from bot.commands.useraname import username_command, Username, name_change
from bot.commands.feedback import feedback_command, Feedback, feedback_send


def register_user_commands(router: Router):
    router.message.register(start_command, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(username_command, Command(commands=['username'])),
    router.message.register(name_change, Username.name)
    router.message.register(feedback_command, Command(commands=['feedback']))
    router.message.register(feedback_send, Feedback.feedback)

    router.callback_query.register(call_learn, F.data == 'learn_help')
    router.callback_query.register(call_repeat_choice, F.data == 'repeat_choice_help')
    router.callback_query.register(call_repeat, F.data == 'repeat_help')
    router.callback_query.register(call_repeat_old, F.data == 'repeat_old_help')
    router.callback_query.register(call_statistics, F.data == 'statistics_help')
    router.callback_query.register(call_statistics_list, F.data == 'statistics_list_help')
    router.callback_query.register(call_back, F.data == 'back')

    router.message.register(start_command, F.text == '⏪ Назад')

