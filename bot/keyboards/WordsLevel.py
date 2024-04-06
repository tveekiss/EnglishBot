from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

level_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='a1'
        ),
        KeyboardButton(
            text='a2'
        )
    ], [
        KeyboardButton(
            text='b1'
        ),
        KeyboardButton(
            text='b2'
        )
    ], [
        KeyboardButton(
            text='c1'
        ),
        KeyboardButton(
            text='c2'
        )
    ]
],resize_keyboard=True, one_time_keyboard=True)
