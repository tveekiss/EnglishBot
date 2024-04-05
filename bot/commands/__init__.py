__all__ = ['register_user_commands', 'commands_list']

from aiogram import Router
from aiogram.filters import Command

from bot.commands.start import start_command
from bot.commands.help import help_command


def register_user_commands(router: Router):
    router.message.register(start_command, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))

