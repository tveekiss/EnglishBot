from aiogram.types import Message
from bot.keyboards import repeat_kb


async def repeat_choice(message: Message):
    await message.answer('выберите какие слова вы хотите повторить:'
                         'новые слова - те, которые вы выучили недавно и не повторяли\n'
                         'старые слова - те, которые вы выучили давно, и хотите проверить свою память',
                         reply_markup=repeat_kb)
