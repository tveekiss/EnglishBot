import random

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards import create_kb, start_keyboard

from bot.database import WordsDb
from bot.education import Words


class RepeatOld(StatesGroup):
    answer = State()


def get_word(word_list):
    random.shuffle(word_list)
    for word in word_list:
        yield word[1], word[2]


async def repeat_old(message: Message, state: FSMContext):
    user_words = WordsDb(message.from_user.id)
    words_list = user_words.get_repeat_old_list()
    words = get_word(words_list)
    if len(words_list) == 0:
        await message.answer('Вы пока не выучили новые слова')
        return
    await message.answer('Повторение - мать учения')
    difficult = {}
    for word in words_list:
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
    await start_repeat_old(message, state)


async def start_repeat_old(message: Message, state: FSMContext):
    context_data = await state.get_data()
    user_words = WordsDb(message.from_user.id)
    words: get_word = context_data.get('words')
    try:
        eng, rus = next(words)
    except StopIteration:
        await message.answer('Слова на повторение закончились', reply_markup=start_keyboard)
        return
    db = context_data.get('db_words')
    answers = db.random_answers(rus)
    await state.update_data(rus=rus, eng=eng, answers=answers)
    kb = create_kb(answers, 2)
    await message.answer(f'Как переводится слово {eng}?', reply_markup=kb)
    await state.set_state(RepeatOld.answer)


async def result_repeat_old(message: Message, state: FSMContext):
    if message.text == 'Закончить повторение':
        await message.answer('Заканчиваем повторение', reply_markup=start_keyboard)
        await state.clear()
        return
    contest_data = await state.get_data()
    rus = contest_data.get('rus')
    answers = contest_data.get('answers')
    if message.text == rus:
        await message.answer('Правильный ответ!')
    elif message.text in answers:
        await message.answer(f'Неправильно! Правильный ответ: {rus}')
    else:
        await message.answer('Нет такого варианта ответа')
        await state.set_state(RepeatOld.answer)
        return
    await start_repeat_old(message, state)

