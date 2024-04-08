from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database import WordsDb
from bot.keyboards import stat_keyboard


async def statistics(message: Message):
    db = WordsDb(message.from_user.id)
    await message.answer(text=db.get_stat(), reply_markup=stat_keyboard)


async def old_statistics(message: Message):
    db = WordsDb(message.from_user.id)
    words = db.get_repeat_old_list()
    if len(words) == 0:
        await message.answer(text="У вас пока нету выученных слов")
        return
    text = ''
    word_list = {}
    difficult_list = {}
    for word in words:
        difficult = word[0]
        eng = word[1]
        rus = word[2]
        date = word[4]

        if date in word_list.keys():
            word_list[date].append([eng, rus])
        else:
            word_list[date] = [[eng, rus]]

        if date in difficult_list.keys():
            if difficult in difficult_list[date].keys():
                difficult_list[date][difficult] += 1
            else:
                difficult_list[date][difficult] = 1
        else:
            difficult_list[date] = {difficult: 1}

    for date_word in word_list.keys():
        text += f'Выученно {date_word}:\n\n'
        for difficult, value in difficult_list[date_word].items():
            text += f'{difficult}: {value}\n'
        text += '\n'
        for word in word_list[date_word]:
            text += f'{word[0]} - {word[1]}\n'
        text += '\n'

    await message.answer(text, reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]],
                                                                resize_keyboard=True))
