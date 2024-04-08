from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.keyboards import level_kb, create_kb, start_keyboard


from bot.education.classes import Words
from bot.database import WordsDb


class Level(StatesGroup):
    level = State()


class Test(StatesGroup):
    answer = State()


async def starting(message: Message, state: FSMContext):
    await message.answer('Хорошо, я буду отправлять тебе слова на английском языке,'
                         ' а ты должен(а) будешь выбрать правильный вариант снизу, вот так все просто!'
                         ' Слова, в которых ты допустишь ошибку, я добавлю в повторение, '
                         'что бы в будущем смог их снова повторить и отточить свои навыки!')
    await message.answer("""
Но для начала, выбери уровень английских слов:

По европейской классификации выделяются три основных типа: 
начинающий, средний и продвинутый (Basic, Independent, Proficient).

Эти уровни английского языка делятся еще на две категории.

Таким образом получается 6 уровней:
A1 (Elementary) — базовый;
A2 (Pre Intermediate) — хороший базовый;
B1 (Intermediate) — средний;
B2 (Upper Intermediate) — хороший средний;
C1 (Advanced) — высокий;
C2 (Proficiency) — самый высокий, уровень носителя.
                         """, reply_markup=level_kb)
    await state.set_state(Level.level)


async def learning(message: Message, state: FSMContext):
    await message.answer('Отличный выбор! Теперь я буду давать тебе слова на английском языке,'
                         ' а ты будешь пытаться их переводить')
    await state.update_data(level=message.text)
    db = WordsDb(message.from_user.id)
    words = Words(message.text, message.from_user.id)
    await state.update_data(words=words, db=db)
    eng, rus, answers = words.random_word()
    await state.update_data(rus=rus, eng=eng)
    await testing(message, state)


async def testing(message: Message, state: FSMContext):
    context_data = await state.get_data()
    level = context_data.get('level')
    cl_words: Words = context_data.get('words')
    user_words: WordsDb = context_data.get('db')
    eng, rus, answers = cl_words.random_word()
    if user_words.check_word(eng, rus):
        await testing(message, state)
        return
    await state.update_data(rus=rus, eng=eng, answers=answers)
    kb = create_kb(answers)
    await message.answer(f'Как переводится слово: {eng}?', reply_markup=kb)
    await state.set_state(Test.answer)


async def result(message: Message, state: FSMContext):
    repeat = 1
    context_data = await state.get_data()
    rus = context_data.get('rus')
    answers = context_data.get('answers')
    if message.text == 'Закончить обучение':
        await state.clear()
        await message.answer('Заканчиваю. Не хотите повторить слова?', reply_markup=start_keyboard)
        return
    elif message.text == rus:
        await message.answer('Правильный ответ')
    elif message.text in answers:
        await message.answer(f"Неправильно. Правильный ответ - {rus}. \n"
                             f"Запишу на повторение")
        repeat = 2
    else:
        await message.answer('Нет такого варианта ответа!')
        await state.set_state(Test.answer)
        return

    db: WordsDb = context_data.get('db')
    level = context_data.get('level')
    eng = context_data.get('eng')
    db.insert_word(level, eng, rus, repeat)
    await testing(message, state)

