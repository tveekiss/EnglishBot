import random

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

from bot.keyboards import create_kb, start_keyboard

from bot.database import users, words


class RepeatOld(StatesGroup):
    answer = State()


async def get_word(word_list_id):
    words_list = []
    for word in word_list_id:
        words_list.append(await words.get_word_by_id(word))
    print(words_list[0])
    for word in words_list:
        answers = [word.rus]
        while len(answers) != 4:
            answer = random.choice(words_list)
            if answer.rus in answers:
                continue
            answers.append(answer.rus)
        yield word, answers


async def repeat_old(message: Message, state: FSMContext):
    word_list = await words.repeat_old_list(message.from_user.id)
    if len(word_list) < 4:
        await message.answer('Вы пока не выучили достаточно слов (нужно минимум 4)🙁')
        return
    gen = get_word(word_list)
    await message.answer('Повторение - мать учения 🧠')
    await state.update_data(gen=gen)
    await testing_old(message, state)


async def testing_old(message: Message, state: FSMContext):
    context_data = await state.get_data()
    gen = context_data['gen']
    try:
        word, answers = await gen.__anext__()
    except StopAsyncIteration:
        await message.answer('Мы повторили все слова ☺️\n\nВыбери действие снизу ⤵️', reply_markup=start_keyboard)
        await state.clear()
        return
    await message.answer(f'Как переводится слово <b>{word.eng}</b> ?', reply_markup=create_kb(answers, 2),
                         parse_mode=ParseMode.HTML)
    await state.update_data(answers=answers, word_id=word.id, gen=gen)
    await state.set_state(RepeatOld.answer)


async def result_old(message: Message, state: FSMContext):
    context_data = await state.get_data()
    word_id = context_data['word_id']
    word = await words.get_word_by_id(word_id)
    answers = context_data['answers']
    if message.text == '⏪ Закончить повторение':
        await message.answer('✨ Заканчиваю ✨', reply_markup=start_keyboard)
        await message.answer('Выбери действие снизу ⤵️')
        await state.clear()
        return
    if message.text == word.rus:
        await message.answer('✅ Правильно')
    elif message.text in answers:
        await message.answer(f'❌ Неверно, правильный ответ: <b>{word.rus}</b>', parse_mode=ParseMode.HTML)
    else:
        await message.answer('❗️ Нет такого варианта ответа!')
        await state.set_state(RepeatOld.answer)
        return
    await testing_old(message, state)
