from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stat_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='⏪ Назад'
        )
    ]
], resize_keyboard=True)
