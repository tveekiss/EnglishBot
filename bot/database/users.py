from datetime import datetime

from bot.database.db import async_session, Users, UserWords, Words
from sqlalchemy import select, update

from bot.database import words

from bot.keyboards import emoji


async def get_user_by_id(tg_id) -> Users:
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.telegram_id == tg_id))

        print(user)
        return user


async def add_user(tg_id, username):
    async with async_session() as session:
        user = Users(username=username, telegram_id=tg_id)
        session.add(user)
        await session.commit()


async def edit_username(tg_id, username):
    async with async_session() as session:
        await session.execute(update(Users).where(Users.telegram_id == tg_id).values(username=username))
        await session.commit()


async def get_statistics(tg_id):
    async with async_session() as session:
        user = await get_user_by_id(tg_id)
        words_id = await session.execute(select(UserWords.word_id)
                                         .where(
            (UserWords.user_id == user.id) & (UserWords.repeat == 0)))
        words_id = words_id.scalars().unique().all()
        if len(words_id) == 0:
            return None
        print(words_id)
        words_list = [await words.get_word_by_id(word_id) for word_id in words_id]
        all_learn_words = await session.execute(select(UserWords.date)
                                                .where((UserWords.user_id == user.id) & (UserWords.repeat == 0)))
        all_learn_words = all_learn_words.scalars().all()

        len_words = len(all_learn_words)
        today = 0
        month = 0
        word_dict = {}

        today_date = datetime.strftime(datetime.now(), '%d.%m.%Y')
        for date in all_learn_words:
            if date == today_date:
                today += 1
            if date.split('.')[1] == today_date.split('.')[1] and date.split('.')[2] == today_date.split('.')[2]:
                month += 1

        for word in words_list:

            if word.difficulty in word_dict.keys():
                word_dict[word.difficulty] += 1
            else:
                word_dict[word.difficulty] = 1

        text = '✍️ Твоя статистика за все время:\n\n'
        text += f'🧠 Всего слов: <b>{len_words}</b>\n\n\n'
        text += ''.join([f'{emoji[key.upper()]} <b>{key.upper()}: {value}</b>\n\n' for key, value in word_dict.items()])
        text += f'\n🗓️ Выучено за текущий месяц: <b>{month}</b>\n'
        text += f'\n🌟 Выучено за сегодня: <b>{today}</b>\n'
        return text


async def get_old_list(tg_id):
    user = await get_user_by_id(tg_id)
    async with async_session() as session:
        words_list = await session.execute(select(UserWords)
                                           .where((UserWords.user_id == user.id) & (UserWords.repeat == 0))
                                           .order_by(UserWords.date.desc()))
        words_list = words_list.scalars().unique().all()
        result_list = []
        for word in words_list:
            result_list.append([word.word.difficulty, word.word.rus, word.word.eng, word.date])
        return result_list



