import random
import sqlite3
import os
import datetime

from bot.database.register import Users
from bot.keyboards.WordsLevel import levels



class WordsDb:
    def __init__(self, tg_id):
        self.user_id = tg_id
        self.conn = sqlite3.connect(os.getenv('db_words_name'))
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = f"""
                CREATE TABLE IF NOT EXISTS words_{self.user_id}(
                difficult TEXT NOT NULL,
                eng TEXT NOT NULL,
                rus TEXT NOT NULL,
                repeat INTEGER DEFAULT 0,
                datetime TIMESTAMP);
            """
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании', Error)

    def insert_word(self, difficulty, word, rus, repeat):
        self.cursor.execute(f"""INSERT INTO words_{self.user_id} VALUES (?, ?, ?, ?, ?)""",
                            (difficulty, word, rus, repeat, datetime.date.today()))
        self.conn.commit()

    def check_word(self, eng, rus):
        self.cursor.execute(f"SELECT * FROM words_{self.user_id} WHERE eng = ? AND rus = ?", (eng, rus))
        result = self.cursor.fetchone()
        return result is not None

    def get_repeat_list(self):
        words = self.cursor.execute(f"SELECT * FROM words_{self.user_id} WHERE repeat > 0")
        return words.fetchall()

    def update_repeat(self, eng, rus, result):
        self.cursor.execute(f"UPDATE words_{self.user_id} SET repeat = repeat + ? WHERE eng =? AND rus =?",
                            (result, eng, rus))
        self.conn.commit()

    def __del__(self):
        count = len(self.cursor.execute(f'SELECT * FROM words_{self.user_id} WHERE repeat = 0;').fetchall())
        user = Users().update_words(self.user_id, count)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_stat(self):
        self.cursor.execute(f'SELECT difficult, datetime FROM words_{self.user_id} WHERE repeat = 0;')
        all_learn_words = self.cursor.fetchall()
        today = 0
        for word in all_learn_words:
            if word[1] == str(datetime.datetime.today().date()):
                today += 1

        levels_stat = {}

        for word in all_learn_words:
            word = word[0]
            if word in levels_stat.keys():
                levels_stat[word] += 1
            else:
                levels_stat[word] = 1
        text = f"Статистика\nСлов за все время: {len(all_learn_words)}\n"
        text += 'Количество слов в каждом уровне:\n'
        text += ''.join([f'{k}: {v}\n' for k, v in levels_stat.items()])
        text += f'За сегодня: {today}'
        return text


if __name__ == '__main__':
    db = WordsDb(1778058617)
    print(db.get_repeat_list())
