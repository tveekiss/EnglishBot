from aiogram.types import Message
from bot.keyboards import start_keyboard
from bot.database import Users
from bot.keyboards import first_button


async def start_command(message: Message):
    db = Users()
    user = db.check_user(message.from_user.id)
    if user:
        await message.answer(
            f'Привет {user[1]}! Выбери действие снизу!',
            reply_markup=start_keyboard
        )
    else:
        await message.answer('Привет! Этот бот сделан для изучение английских слов!'
                             ' Нажми кнопку ниже что бы начать учебу!', reply_markup=first_button)
