from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.keyboards import start_keyboard
from bot.database import Users


class Register(StatesGroup):
    username = State()


async def start_register(message: Message, state: FSMContext):
    db = Users()
    user = db.check_user(message.from_user.id)
    if not user:
        await message.answer('Привет. Вижу ты тут первый раз. Введи имя для того что бы я знал как к тебе обращаться')
        await state.set_state(Register.username)


async def register_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    username_data = await state.get_data()
    username = username_data.get('username')
    db = Users()
    db.add_user(username, message.from_user.id)
    await state.clear()
    await message.answer(f'Приятно познакомиться {message.text}! Регистрация закончена и теперь выбери действие снизу',
                         reply_markup=start_keyboard)


