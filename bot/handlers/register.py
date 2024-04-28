from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import start_keyboard
from bot.database import users
from aiogram.types import ReplyKeyboardRemove
from aiogram.enums import ParseMode


class Register(StatesGroup):
    username = State()


async def start_register(message: Message, state: FSMContext):
    user = await users.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer(
            f'Привет! Рад видеть тебя здесь впервые! 😊'
            f'\n\nДавай знакомиться! Назови мне свое имя, чтобы я знал, как к тебе обращаться. 🤖👋'
            '\nИли используй имя твоего аккаунта Telegram 🪄',
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Использовать имя из telegram 🪄')]],
                                             resize_keyboard=True))
        await state.set_state(Register.username)


async def register_name(message: Message, state: FSMContext):
    if message.text == 'Использовать имя из telegram 🪄':
        username = message.from_user.full_name
    else:
        username = message.text
    await users.add_user(username=username, tg_id=message.from_user.id)
    await state.clear()
    await message.answer(
        f'Привет, <b>{username}</b>! 👋 Добро пожаловать в нашего бота!'
        f'\n\n Чтобы узнать что я умею, введи: /help 🤖'
        f'\n\n<b>P.S.</b> Так же ты можешь отправить пожелание или сообщение об ошибке по команде: /feedback 😊',
        reply_markup=start_keyboard, parse_mode=ParseMode.HTML)
