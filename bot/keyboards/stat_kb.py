from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stat_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Посмотреть базу выученных слов'
        )
    ], [
        KeyboardButton(
            text='Назад'
        )
    ]
], resize_keyboard=True)
