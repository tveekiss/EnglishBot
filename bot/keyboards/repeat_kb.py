from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

repeat_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Повторить новые слова'
        )
    ], [
        KeyboardButton(
            text='Повторить старые слова'
        )
    ], [
        KeyboardButton(
            text='Назад'
        )
    ]
], resize_keyboard=True)
