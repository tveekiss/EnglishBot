from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Учить слова'
        ),
        KeyboardButton(
            text='Переводчик'
        )
    ], [
        KeyboardButton(
            text='Статистика'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True)
