import random
import sqlite3
import os

from bot.database.register import Users



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
                repeat INTEGER DEFAULT 0);
            """
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании', Error)

    def insert_word(self, difficulty, word, rus, repeat):
        self.cursor.execute(f"""INSERT INTO words_{self.user_id} VALUES (?, ?, ?, ?)""", (difficulty, word, rus, repeat))
        self.conn.commit()

    def check_repeat(self, difficulty, word):
        check = self.cursor.execute("SELECT * FROM words_{self.user_id} WHERE eng = ?", (word,))
        return check.fetchone() is not None

    def get_repeat_list(self):
        words = self.cursor.execute(f"SELECT * FROM words_{self.user_id} WHERE repeat > 0")
        return words.fetchall()

    def update_repeat(self, eng, rus):
        self.cursor.execute(f"UPDATE words_{self.user_id} SET repeat = repeat - 1 WHERE eng =? AND rus =?", (eng, rus))
        self.conn.commit()

    def __del__(self):
        count = len(self.cursor.execute(f'SELECT * FROM words_{self.user_id} WHERE repeat = 0;').fetchall())
        user = Users().update_words(self.user_id, count)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = WordsDb(1778058617)
    print(db.get_repeat_list())
