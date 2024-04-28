from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from bot.keyboards import start_keyboard, username_kb
from bot.database import users, Users


class Username(StatesGroup):
    name = State()


async def username_command(message: Message, state: FSMContext):
    user: Users = await users.get_user_by_id(message.from_user.id)
    await message.answer('Хочешь, чтобы я тебя назвал по-другому? 🤔 \nПросто напиши мне новое имя! 📝'
                         '\nИли используй имя твоего аккаунта Telegram 🪄'
                         f'\nТекущее имя: <b>{user.username}</b>',
                         reply_markup=username_kb, parse_mode=ParseMode.HTML)
    await state.set_state(Username.name)


async def name_change(message: Message, state: FSMContext):
    if message.text == '⏪ Назад':
        user = await users.get_user_by_id(message.from_user.id)
        await message.answer(f'Хорошо, оставайся <b>{user.username}</b> 🤝',
                             reply_markup=start_keyboard, parse_mode=ParseMode.HTML)
        await state.clear()
        return
    elif message.text == 'Использовать имя из telegram 🪄':
        username = message.from_user.full_name
    else:
        username = message.text
    await users.edit_username(message.from_user.id, username)
    await message.answer(f'С этого момента я буду называть тебя <b>{username}</b>! 🪄✨',
                         reply_markup=start_keyboard, parse_mode=ParseMode.HTML)
    await state.clear()

