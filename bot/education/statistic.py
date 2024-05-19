from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database import users
from bot.keyboards import stat_keyboard, emoji
from aiogram.enums import ParseMode


async def statistic(message: Message):
    text = await users.get_statistics(message.from_user.id)
    if text is None:
        await message.answer('Вы пока не выучили не одного слова 🙁')
        return
    await message.answer(text, reply_markup=stat_keyboard, parse_mode=ParseMode.HTML)
