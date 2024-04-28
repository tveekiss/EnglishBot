from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

from bot.keyboards import create_kb, start_keyboard

from bot.database import words


class Repeat(StatesGroup):
    answer = State()


async def repeat_new(message: Message, state: FSMContext):
    if not await words.check_repeat(message.from_user.id):
        await message.answer('Нету слов на повторение ️️🙁')
        return
    await message.answer('📚✨ Привет! В разделе "Закрепление новых слов" ты можешь закрепить слова,'
                         ' которые уже выучил. Если сделал ошибку, повтори слово дважды,'
                         ' чтобы закрепить знание. Если все верно, достаточно одного повторения.'
                         ' Учи и совершенствуйся! 🧠💪🏼')
    await testing_repeat(message, state)


async def testing_repeat(message: Message, state: FSMContext):
    word_id, answers = await words.repeat_word(message.from_user.id)
    if word_id is None:
        print('Нету слов')
        await message.answer('🎉 Слова закончились 🎉\n\nВыбери действие снизу ⤵️', reply_markup=start_keyboard)
        await state.clear()
        return
    word = await words.get_word_by_id(word_id)
    await message.answer(f'Как переводится слово <b>{word.eng}</b> ?', reply_markup=create_kb(answers, 1),
                         parse_mode=ParseMode.HTML)
    await state.update_data(word_id=word_id, answers=answers)
    await state.set_state(Repeat.answer)


async def result_repeat(message: Message, state: FSMContext):
    rep = 0
    context_data = await state.get_data()
    word_id = context_data['word_id']
    answers = context_data['answers']
    word = await words.get_word_by_id(word_id)
    if message.text == '⏪ Закончить закрепление':
        await message.answer('✨ Заканчиваю ✨', reply_markup=start_keyboard)
        await message.answer('выбери действие снизу ⤵️')
        await state.clear()
        return
    if message.text == word.rus:
        await message.answer('✅ Правильно ')
        rep -= 1
    elif message.text in answers:
        await message.answer(f'❌ Неверно, правильный ответ: <b>{word.rus}</b> ', parse_mode=ParseMode.HTML)
        rep += 1
    else:
        await message.answer('❗️ Нет такого варианта ответа')
        await state.set_state(Repeat.answer)
        return

    await words.edit_repeat(message.from_user.id, word_id, rep)
    await testing_repeat(message, state)
