from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database import users
from bot.keyboards import stat_keyboard, emoji
from aiogram.enums import ParseMode


async def statistic(message: Message):
    text = await users.get_statistics(message.from_user.id)
    if text is None:
        await message.answer('Вы пока не выучили не одного слова 🙁')
        return
    await message.answer(text, reply_markup=stat_keyboard, parse_mode=ParseMode.HTML)


async def old_statistics(message: Message):
    words = await users.get_old_list(message.from_user.id)

    text = ''
    word_list = {}
    difficult_list = {}
    for word in words:
        difficult = word[0]
        eng = word[1]
        rus = word[2]
        date = word[3]

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
        text += f'📚 Выученно {date_word}:\n\n'
        for difficult, value in difficult_list[date_word].items():
            text += f'{emoji[difficult.upper()]} <b>{difficult}: {value}</b>\n'
        text += '\n'
        for word in word_list[date_word]:
            text += f'<b>{word[0]}</b> - <b>{word[1]}</b>\n'
        text += '\n'

    await message.answer(text, reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='⏪ Назад')]],
                                                                resize_keyboard=True), parse_mode=ParseMode.HTML)
