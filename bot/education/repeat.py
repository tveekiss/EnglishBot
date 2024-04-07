import random

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import create_kb, start_keyboard

from bot.database import WordsDb
from bot.education import Words


class Repeat(StatesGroup):
    answer = State()


async def repeat(message: Message, state: FSMContext):
    await message.answer('Хорошо, давай повторим слова')
    user_words = WordsDb(message.from_user.id)
    words = user_words.get_repeat_list()
    print(words)
    if len(words) == 0:
        await message.answer('Нету слов на повторение', reply_markup=start_keyboard)
        return
    await message.answer(f'Количество слов на повторение: {len(words)}')
    difficult = {}
    for word in words:
        if word[0] in difficult.keys():
            difficult[word[0]] += 1
        else:
            difficult[word[0]] = 1
    max_difficult = max(difficult.values())
    level = None
    for key, value in difficult.items():
        if value == max_difficult:
            level = key
            break
    db_words = Words(level, message.from_user.id)

    await state.update_data(words=words, user_words=user_words, db_words=db_words)
    await start_repeat(message, state)


async def start_repeat(message: Message, state: FSMContext):
    context_data = await state.get_data()
    user_words = WordsDb(message.from_user.id)
    words = user_words.get_repeat_list()
    if all(word[3] == 0 for word in words):
        await message.answer('Нету слов для повторения', reply_markup=start_keyboard)
        await state.clear()
        return
    word = random.choice(words)
    if word[3] == 0:
        await start_repeat(message, state)
    else:
        eng, rus = word[1], word[2]
        db = context_data.get('db_words')
        answers = db.random_answers(rus)
        await state.update_data(rus=rus, eng=eng)

        kb = create_kb(answers)
        await message.answer(f'Как переводится слово {eng}?', reply_markup=kb)
        await state.set_state(Repeat.answer)


async def resut_repeat(message: Message, state: FSMContext):
    if message.text == 'Закончить':
        await message.answer('Заканчиваем повторение', reply_markup=start_keyboard)
        await state.clear()
        return
    context_data = await state.get_data()
    words = context_data.get('words')
    rus = context_data.get('rus')
    eng = context_data.get('eng')
    if rus == message.text:
        await message.answer('Правильный ответ!')
        result = -1
    else:
        await message.answer(f'Неправильно! Правильный ответ: {rus}')
        result = 1
    for i, word in enumerate(words):
        if word[1] == eng and word[2] == rus:
            updated_word = (word[0], word[1], word[2], word[3] + result)  # Создаем новый кортеж с обновленным значением
            words[i] = updated_word  # Заменяем старый кортеж на новый в списке
            break
    db: WordsDb = context_data.get('user_words')
    db.update_repeat(eng, rus, result)
    await start_repeat(message, state)


