from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

username_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Использовать имя из telegram 🪄'
        )
    ], [
        KeyboardButton(
            text='⏪ Назад'
        )
    ]
], resize_keyboard=True)
