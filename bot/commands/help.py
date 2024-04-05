from aiogram.types import Message


async def help_command(message: Message):
    await message.answer('это помощь с ботом (потом придумаю чет напишу)')
