from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import start_keyboard
from bot.database import users, words
from bot.handlers import start_register
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State



class Feedback(StatesGroup):
    feedback = State()


async def feedback_command(message: Message, state: FSMContext):
    admin = 452158224
    user = await users.get_user_by_id(message.from_user.id)
    if message.from_user.id != admin:
        await message.answer(
            f'Привет, <b>{user.username}</b>! 👋 \nОтправь мне сообщение о пожеланиях или о проблеме'
            f' и прикрепи фото проблемы что бы я это исправил! ⤵️',
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='⏪ Назад')]],
                                             resize_keyboard=True), parse_mode=ParseMode.HTML)
        await state.set_state(Feedback.feedback)


async def feedback_send(message: Message, state: FSMContext):
    admin = 452158224
    user = await users.get_user_by_id(message.from_user.id)
    if message.text == '⏪ Назад':
        await message.answer(
            f'Привет, <b>{user.username}</b>! 👋 \nВыбери действие ниже ⤵️',
            reply_markup=start_keyboard, parse_mode=ParseMode.HTML)
        await state.clear()
        return
    all_words_len = len(await words.get_words_id_list(message.from_user.id))
    repeat_len = len(await words.repeat_old_list(message.from_user.id))
    from bot.main import bot
    await bot.send_message(admin, f'❗️ Сообщение от пользователя: <b>{message.from_user.username}</b>\n'
                                  f'id пользователя: <b>{message.from_user.id}</b>\n'
                                  f'количество выученных слов: <b>{all_words_len}</b>\n'
                                  f'Количество слов в повторении: <b>{repeat_len}</b>', parse_mode=ParseMode.HTML)
    await message.copy_to(admin)
    await message.answer('Сообщение отправлено! Спасибо за обратную связь 🤝❤️', reply_markup=start_keyboard)
    await state.clear()
