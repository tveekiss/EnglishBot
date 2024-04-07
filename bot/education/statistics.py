from aiogram.types import Message
from bot.database import WordsDb
from bot.keyboards import start_keyboard


async def statistics(message: Message):
    db = WordsDb(message.from_user.id)
    await message.answer(text=db.get_stat(), reply_markup=start_keyboard)