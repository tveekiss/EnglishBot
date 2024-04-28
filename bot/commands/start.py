from aiogram.types import Message
from bot.keyboards import start_keyboard
from bot.database import users
from bot.handlers import start_register
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode



async def start_command(message: Message, state: FSMContext):
    user = await users.get_user_by_id(message.from_user.id)
    await message.answer(
        f'Привет, <b>{user.username}</b>! 👋 \nВыбери действие ниже ⤵️',
        reply_markup=start_keyboard, parse_mode=ParseMode.HTML)
