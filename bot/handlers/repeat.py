from aiogram.types import Message
from bot.keyboards import repeat_kb
from aiogram.enums import ParseMode


async def repeat_choice(message: Message):
    await message.answer('''
📚✨ Хочешь повторить слова и улучшить свой словарный запас? Выбери, что тебе больше подходит:
1️⃣ "<b>Новые слова</b>" - те, которые ты недавно выучил и еще не повторял. Погнали учить новое!
2️⃣ "<b>Старые слова</b>" - те, которые ты выучил давно и хочешь проверить свою память. Давай вспомним старое! 🧠💪🏼
    ''', reply_markup=repeat_kb, parse_mode=ParseMode.HTML)
