from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

first_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Начать'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True)
