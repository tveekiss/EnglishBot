from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random


def create_kb(answers, end) -> ReplyKeyboardMarkup:
    ends = ['обучение', 'закрепление', 'повторение']
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
                text=f'Закончить ' + (ends[end])
            )
        ]
    ], resize_keyboard=True)
    return kb
