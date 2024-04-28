from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📚 Учить слова'
        ),
        KeyboardButton(
            text='🧠 Повторить'
        )
    ], [
        KeyboardButton(
            text='✍️ Статистика'
        )
    ]
], resize_keyboard=True)
