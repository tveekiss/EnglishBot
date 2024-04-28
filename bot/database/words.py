import random

from bot.database.db import async_session, Users, Words, UserWords
from bot.database import users
from sqlalchemy import select, update
from sqlalchemy.sql.expression import func


async def get_word_by_id(word_id):
    async with async_session() as session:
        return await session.get(Words, word_id)


async def get_words_id_list(tg_id):
    user = await users.get_user_by_id(tg_id)
    async with async_session() as session:
        words_list_id = await session.execute(select(UserWords.id).where(UserWords.user_id == user.id))
        words_list_id = words_list_id.scalars().unique().all()

        return words_list_id


async def random_word(tg_id, level):
    async with async_session() as session:
        level = level.split(' ')[1]
        user = await users.get_user_by_id(tg_id)
        result = await session.execute(select(UserWords.word_id).where(UserWords.user == user))
        link_list = result.scalars().all()
        print(link_list)
        result = await session.execute(
            select(Words).where((Words.difficulty == level) & (Words.id.not_in(link_list))).limit(15))
        word_list = result.scalars().unique().all()
        print(word_list)
        words = random.sample(word_list, k=4)
        print(words)
        current_word = words[0]
        answers = [word.rus for word in words]
        return current_word.id, answers


async def add_word(tg_id, word_id, repeat):
    async with async_session() as session:
        user = await users.get_user_by_id(tg_id)
        word = await get_word_by_id(word_id)
        link = UserWords(repeat=repeat, word=word)
        user.words.append(link)
        session.add(link)
        await session.commit()


async def check_repeat(tg_id):
    async with async_session() as session:
        user = await users.get_user_by_id(tg_id)
        result = await session.execute(select(UserWords).where((UserWords.repeat > 0) & (UserWords.user == user)))
        words_list = result.scalars().unique().all()
        return not len(words_list) == 0


async def repeat_word(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.telegram_id == tg_id))
        print(user)
        words_list = await session.execute(select(UserWords).where((UserWords.repeat > 0) & (UserWords.user == user)))
        words_list = words_list.scalars().unique().all()
        if len(words_list) == 0:
            return None, None
        word = random.choice(words_list)
        word = word.word
        answers_list = await session.execute(select(UserWords).where(UserWords.user == user))
        answers_list = answers_list.scalars().unique().all()
        answers = []
        if len(answers_list) < 4:
            answers = await (session.execute(select(Words.rus)
                                             .where(Words.difficulty == word.difficulty)
                                             .order_by(func.random()).limit(3)))
            answers = answers.scalars().unique().all()
            answers.append(word.rus)
        else:
            answers.append(word.rus)
            random.shuffle(answers_list)
            for answer_word in answers_list:
                if len(answers) == 4:
                    break
                if answer_word.word.rus != word.rus:
                    print(2)
                    answers.append(answer_word.word.rus)
        return word.id, answers


async def edit_repeat(tg_id, word_id, repeat):
    async with async_session() as session:
        user = await users.get_user_by_id(tg_id)
        word = await get_word_by_id(word_id)
        res_repeat = await session.execute(select(UserWords.repeat)
                                           .where((UserWords.word == word) & (UserWords.user == user)))
        res_repeat = res_repeat.scalar()
        print(res_repeat)
        await session.execute(update(UserWords).where((UserWords.word == word) & (UserWords.user == user))
                              .values(repeat=res_repeat + repeat))
        await session.commit()


async def repeat_old_list(tg_id):
    async with async_session() as session:
        user = await users.get_user_by_id(tg_id)
        words_list = await session.execute(select(UserWords).where((UserWords.repeat == 0) & (UserWords.user == user)))
        words_list = words_list.scalars().unique().all()
        random.shuffle(words_list)
        result_list = [word.word.id for word in words_list]
        return result_list
