from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
)

help_dict = {
    'Учить слова': """
Изучение слов является самой главной функцией бота
Реализованно оно следующим образом:

1. Бот спрашивает у вас какой уровень английских слов вы
 хотите выучить и дает инструкцию по выбору уровня;

2. После этого отправляет вам слово и варианты перевода;

3. После ответа, бот записывает слово в закрепление,
независимо от того правильный ответ или нет.
(закрепление находится в "Повторить" -> "Закрепить новые слова)

если ответ правильный - повторить надо будет 1 раз,
если не правильный, повторить надо будет 2 раза.


"Учить слова"
""",
    'Повторить': """
Повторение является важным и ключевым моментов в 
изучении любого иностранного языка.


Если вы хотите закрепить новые слова что бы они 
отображались в статистики считались полностью выученными, 
выберите "Повторить" -> "Закрепить новые слова"

А если хотите повторить уже полностью выученные слова,
тогда перейдите в "Повторить" -> "Повторить старые слова"


"Повторить"
""",
    'Закрепить новые слова': """
Здесь вы сможете закрепить изученные слова для того
что бы окончательно из выучить.
реализовано так:

1. Бот отправляет слово которые вы встретили в изучении
(подробнее про изучение слов в "учить слова")

2. Вы выбираете вариант ответа

3. Если ответ правильный, количество повторении слов уменьшается на 1,
а если неправильный, то увеличивается на 1.

Количество повторений слова можно узнать в сообщении.


"Повторить" > "Закрепить новые слова"
""",
    'Повторить старые слова':"""
Здесь вы сможете повторить ранее выученные слова.
как устроенно?

1. Бот дает слово

2. Вы даете ответ

3. Бот говорит правильно или нет


Вроде... все ясно, да?..


"Повторить" > "Повторить старые слова"
""",
    'Статистика': """
Здесь будет показана вся ваша статистика, а именно:

1. Количество выученных слов

2. количество выученных слов в каждой категории

3. Количество выученных слов за месяц

4. Количество выученных слов за сегодня


"Статистика"
""",
    'Посмотреть базу выученных слов': """
Здесь вы увидите список всех выученных вами слов,
которая будет отсортирована по датам
и с количеством выученных слов по уровням
 
 
"Статистика" > "Посмотреть базу выученных слов"
"""
}


async def help_command(message: Message):
    buttons = [
        [
            InlineKeyboardButton(text='Учить слова', callback_data='learn_help'),
            InlineKeyboardButton(text='Повторить', callback_data='repeat_choice_help'),
        ],[
            InlineKeyboardButton(text='Статистика', callback_data='statistics_help')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer('Привет!\n'
                         'Давай я быстро покажу тебе что я умею\n'
                         'Для это выбери снизу о какой моей функции ты хочешь узнать?', reply_markup=keyboard)


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
        ],[
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
