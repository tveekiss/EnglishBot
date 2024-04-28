from datetime import datetime
import os
import asyncio


from sqlalchemy import ForeignKey, Column, BigInteger, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserWords(Base):
    __tablename__ = 'users_words'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    word_id: Mapped[int] = mapped_column(ForeignKey('words.id', ondelete='CASCADE'))

    repeat: Mapped[int]
    date: Mapped[str] = mapped_column(default=datetime.strftime(datetime.now(), '%d.%m.%Y'))

    user: Mapped['Users'] = relationship(back_populates='words', lazy='joined')
    word: Mapped['Words'] = relationship(back_populates='users', lazy='joined')

    def __repr__(self):
        return f'Пользователь: {self.user}\nСлово: {self.word}\n кол-во повторений: {self.repeat}'


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    telegram_id = Column(BigInteger, unique=True)

    words: Mapped[list['UserWords']] = relationship(back_populates='user', lazy='joined')

    def __repr__(self):

        return f'Имя: {self.username}, tg_id: {self.telegram_id}'

    def get_id(self):
        return self.id


class Words(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    difficulty: Mapped[str]
    eng: Mapped[str]
    rus: Mapped[str]

    users: Mapped[list['UserWords']] = relationship(back_populates='word', lazy='joined')

    def __repr__(self):
        return f'сложность: {self.difficulty}, слово: {self.eng} - {self.rus}'

    @property
    def get_id(self):
        return self.id


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with async_session() as session:
            result = await session.execute(select(Words))
            words = result.scalars().all()
            if len(words) == 0:
                file_list = os.listdir('words')
                print(file_list)
                for file in file_list:
                    with open(os.path.join('words', file), 'r', encoding='utf-8') as f:
                        print(f)
                        for line in f.readlines():
                            print(line)
                            eng, rus = line.split('-')
                            rus = rus[:-1]
                            word = Words(difficulty=file.split('.')[0], eng=eng, rus=rus)
                            session.add(word)
                await session.commit()

if __name__ == '__main__':
    asyncio.run(async_main())
