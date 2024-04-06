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
                mistakes INTEGER DEFAULT 0);
            """
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании', Error)

    def insert_word(self, difficulty, word, rus, mistakes=0):
        self.cursor.execute(f"""INSERT INTO words_{self.user_id} VALUES (?, ?, ?, ?)""", (difficulty, word, rus, mistakes))
        self.conn.commit()

    def check_word(self, difficulty, word):
        word = self.cursor.execute("SELECT * FROM words_{self.user_id}"
                                   " WHERE difficulty = ? AND word = ?", (difficulty, word))
        return word.fetchone() is not None

    def __del__(self):
        count = len(self.cursor.execute(f'SELECT * FROM words_{self.user_id} WHERE mistakes = 0;').fetchall())
        user = Users().update_words(self.user_id, count)
        self.cursor.close()
        self.conn.close()
