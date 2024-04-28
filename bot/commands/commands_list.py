from aiogram.types import BotCommand, BotCommandScopeDefault, Update


async def set_commands_list(bot):
    commands = [
        BotCommand(
            command='start',
            description='Запуск бота'
        ),
        BotCommand(
            command='help',
            description='Помощь в работе с ботом'
        ),
        BotCommand(
            command='username',
            description='Изменить имя пользователя'
        ),
        BotCommand(
            command='feedback',
            description='Отправить пожелание или сообщение об ошибке'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
