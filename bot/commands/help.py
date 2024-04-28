from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
)

help_dict = {
    'Учить слова': """
Привет! 🌟
Хочешь улучшить свой словарный запас на английском? 📚🔍
Давай начнем! Выбери уровень, который хочешь изучать:
1️⃣ Начинающий
2️⃣ Средний
3️⃣ Продвинутый

После выбора уровня я буду отправлять тебе слова с вариантами перевода. Ты готов? 💪🏼

Начнем с первого слова:
Word: Apple
Переведи это слово на русский.

Отлично! 🍎
Запомни, что "Apple" - это "Яблоко".
Теперь это слово добавлено в твое закрепление. Не забудь повторить его в разделе "Закрепить новые слова". 📝

Готов к следующему слову? 🤔


"Учить слова"
""",
    'Повторить': """
Повторение - это 🔑 в изучении любого иностранного языка! 🚀

Если вы хотите закрепить новые слова, чтобы они отображались в статистике как полностью выученные, выберите "Повторить" -> "Закрепить новые слова". 📝

А если хотите повторить уже полностью выученные слова, тогда перейдите в "Повторить" -> "Повторить старые слова". 🔄

Помните, что регулярное повторение поможет вам сделать ваш словарный запас крепче! 💪🏼

Готовы повторить еще слова или продолжим изучение новых? 🤔


"Повторить"
""",
    'Закрепить новые слова': """
🔑 Привет! Здесь ты можешь закрепить изученные слова, чтобы окончательно их выучить! 🧠

📚 Как это работает:
1. Я отправлю тебе слово, которое ты встречал в процессе изучения (подробнее об изучении слов в разделе "Учить слова").
2. Ты выбираешь правильный вариант ответа.
3. Если ответ правильный, количество повторений этого слова уменьшится на 1, а если неправильный - увеличится на 1.

🔢 Текущее количество повторений слова ты можешь узнать в сообщении.


"Повторить" > "Закрепить новые слова"
""",
    'Повторить старые слова': """
🔑 Привет! Здесь ты сможешь повторить ранее выученные слова! 🧠

📚 Как это работает:
1. Я буду давать тебе слово.

2. Ты дашь ответ.

3. Я скажу, правильно ли ты ответил.

Вроде все понятно, да? 😊


"Повторить" > "Повторить старые слова"
""",
    'Статистика': """
📊 Вот тут будет твоя статистика:

1. Общее количество выученных слов 🧠

2. Количество выученных слов в каждой категории 📚

3. Количество выученных слов за месяц 🗓️

4. Количество выученных слов за сегодня 🌟


"Статистика"
""",
    'Посмотреть базу выученных слов': """
📅 Тут для тебя будет список всех слов, которые ты выучил! Они упорядочены по датам и разбиты на уровни

Он будет дополнятся постепенно, после того как ты будешь учить новые слова 🚀
 
"Статистика" > "Посмотреть базу выученных слов"
"""
}


async def help_command(message: Message):
    buttons = [
        [
            InlineKeyboardButton(text='Учить слова', callback_data='learn_help'),
            InlineKeyboardButton(text='Повторить', callback_data='repeat_choice_help'),
        ], [
            InlineKeyboardButton(text='Статистика', callback_data='statistics_help')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer('''
Привет! 🌟
Давай, я покажу на что ты способен! 💪🏼
Выбери ниже, какую мою функцию ты хочешь узнать больше: 🔍🧠
    ''', reply_markup=keyboard)


async def call_learn(call: CallbackQuery):
    button = [
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(text=help_dict['Учить слова'], reply_markup=keyboard)


async def call_repeat_choice(call: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text='Закрепить новые слова', callback_data='repeat_help'),
            InlineKeyboardButton(text='Повторить старые слова', callback_data='repeat_old_help')
        ], [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(text=help_dict['Повторить'], reply_markup=keyboard)


async def call_repeat_old(call: CallbackQuery):
    button = [
        [InlineKeyboardButton(text='Назад', callback_data='repeat_choice_help')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(text=help_dict['Повторить старые слова'], reply_markup=keyboard)


async def call_repeat(call: CallbackQuery):
    button = [
        [InlineKeyboardButton(text='Назад', callback_data='repeat_choice_help')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(text=help_dict['Закрепить новые слова'], reply_markup=keyboard)


async def call_statistics(call: CallbackQuery):
    button = [
        [InlineKeyboardButton(text='Посмотреть базу выученных слов', callback_data='statistics_list_help')],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(text=help_dict['Статистика'], reply_markup=keyboard)


async def call_statistics_list(call: CallbackQuery):
    button = [
        [InlineKeyboardButton(text='Назад', callback_data='statistics_help')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(text=help_dict['Посмотреть базу выученных слов'], reply_markup=keyboard)


async def call_back(call: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text='Учить слова', callback_data='learn_help'),
            InlineKeyboardButton(text='Повторить', callback_data='repeat_choice_help'),
        ],[
            InlineKeyboardButton(text='Статистика', callback_data='statistics_help')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text('Привет!\n'
                                 'Давай я быстро покажу тебе что я умею\n'
                                 'Для это выбери снизу о какой моей функции ты хочешь узнать?', reply_markup=keyboard)
