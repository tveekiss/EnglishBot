from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random


def create_kb(answers) -> ReplyKeyboardMarkup:
    random.shuffle(answers)
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=f'{answers[0]}'
            ),
            KeyboardButton(
                text=f'{answers[1]}'
            )
        ], [
            KeyboardButton(
                text=f'{answers[2]}'
            ),
            KeyboardButton(
                text=f'{answers[3]}'
            )
        ], [
            KeyboardButton(
                text=f'Закончить'
            )
        ]
    ], resize_keyboard=True, one_time_keyboard=True)
    return kb
