from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from bot.keyboards import level_kb, create_kb, start_keyboard

from bot.database import words


class Test(StatesGroup):
    answer = State()
    level = State()


async def starting(message: Message, state: FSMContext):
    if await words.len_learn_words(message.from_user.id) >= 15:
        await message.answer('У вас в очереди на закрепление 15 слов 🙁\n'
                             'Закрепите слова в повторении 🧠')
        return
    await message.answer('🌟📚 Прекрасно! Я буду отправлять тебе слова на английском языке,'
                         ' а ты просто выберешь правильный вариант снизу. 🤗 Ничего сложного!'
                         ' Если где-то ошибешься, не беда - я добавлю это слово в повторение,'
                         ' чтобы ты мог его потом отточить и стать еще лучше! 💪🚀')
    await message.answer("""
Но для начала, выбери уровень английских слов: 🌟

По европейской классификации выделяются три основных типа: 

1️⃣ <b>Basic</b> (начинающий)
2️⃣ <b>Independent</b> (средний)
3️⃣ <b>Proficient</b> (продвинутый)


Эти уровни английского языка делятся еще на две категории. 📚

Таким образом получается 6 уровней:
👶🏻 <b>A1</b> (Elementary) — базовый;
🥱 <b>A2</b> (Pre Intermediate) — хороший базовый;
💡 <b>B1</b> (Intermediate) — средний;
💪🏻 <b>B2</b> (Upper Intermediate) — хороший средний;
🔥 <b>C1</b> (Advanced) — высокий;
😈 <b>C2</b> (Proficiency) — самый высокий, уровень носителя.
                         """, reply_markup=level_kb, parse_mode=ParseMode.HTML)
    await state.set_state(Test.level)


async def introduction(message: Message, state: FSMContext):
    await message.answer('Отлично! 🌟 Приготовься к веселому испытанию! 📚🎉'
                         ' Я буду предлагать тебе английские слова, а ты попробуешь их перевести.'
                         ' Готов начать? 💬💡')
    await state.update_data(level=message.text.lower())
    await testing(message, state)


async def testing(message: Message, state: FSMContext):
    if await words.len_learn_words(message.from_user.id) >= 15:
        await message.answer('У вас в очереди на закрепление 15 слов 🙁\n'
                             'Закрепите слова в повторении 🧠', reply_markup=start_keyboard)
        await state.clear()
        return
    context_data = await state.get_data()
    word_id, answers = await words.random_word(message.from_user.id, level=context_data['level'])
    word = await words.get_word_by_id(word_id)
    print(word)
    print(answers)
    await state.update_data(answers=answers, word=word.id)
    await message.answer(f'Как переводится слово <b>{word.eng}</b> ?', reply_markup=create_kb(answers, 0),
                         parse_mode=ParseMode.HTML)
    await state.set_state(Test.answer)


async def result(message: Message, state: FSMContext):
    context_data = await state.get_data()
    repeat = None
    answers = context_data['answers']
    word = await words.get_word_by_id(context_data['word'])
    print(answers)
    if message.text == '⏪ Закончить обучение':
        await message.answer('✨ Заканчиваю ✨', reply_markup=start_keyboard)
        await message.answer('Выбери действие снизу ⤵️')
        await state.clear()
        return
    if message.text == word.rus:
        repeat = 1
        await message.answer('✅ Правильно ')
    elif message.text in answers:
        repeat = 2
        await message.answer(f'❌ Неверно, правильный ответ: <b>{word.rus}</b> ', parse_mode=ParseMode.HTML)
    else:
        await message.answer('❗️ Нет такого варианта ответа!')
        await state.set_state(Test.answer)
        return

    await words.add_word(message.from_user.id, context_data['word'], repeat)
    await testing(message, state)
