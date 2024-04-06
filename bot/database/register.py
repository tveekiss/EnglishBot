import sqlite3
import os


class Users:
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv("db_name"))
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = """
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                word_count INTEGER DEFAULT 0);
            """
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании', Error)

    def add_user(self, username, telegram_id):
        self.cursor.execute("INSERT INTO users(id, username) VALUES(?, ?)", (telegram_id, username))
        self.conn.commit()

    def check_user(self, telegram_id):
        user = self.cursor.execute('SELECT * FROM users WHERE id = ?', (telegram_id,))
        return user.fetchone()

    def update_words(self, telegram_id, word_count):
        self.cursor.execute('UPDATE users SET word_count = ? WHERE id = ?', (word_count, telegram_id))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
