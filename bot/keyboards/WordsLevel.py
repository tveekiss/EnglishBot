from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

emoji = {
    'A1': '👶🏻',
    'A2': '🥱',
    'B1': '💡',
    'B2': '💪🏻',
    'C1': '🔥',
    'C2': '😈'
}

level_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text=f'{emoji["A1"]} A1'
        ),
        KeyboardButton(
            text=f'{emoji["A2"]} A2'
        )
    ], [
        KeyboardButton(
            text=f'{emoji["B1"]} B1'
        ),
        KeyboardButton(
            text=f'{emoji["B2"]} B2'
        )
    ], [
        KeyboardButton(
            text=f'{emoji["C1"]} C1'
        ),
        KeyboardButton(
            text=f'{emoji["C2"]} C2'
        )
    ], [
        KeyboardButton(
            text='⏪ Назад'
        )
    ]
], resize_keyboard=True)

