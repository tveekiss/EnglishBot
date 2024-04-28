from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

repeat_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🧠 Закрепить новые слова'
        )
    ], [
        KeyboardButton(
            text='🗓️ Повторить старые слова'
        )
    ], [
        KeyboardButton(
            text='⏪ Назад'
        )
    ]
], resize_keyboard=True)
