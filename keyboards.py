from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types
from kbd import db as db

kb = [
    [
        types.KeyboardButton(text="Каталог 📕"),
        types.KeyboardButton(text="Корзина 🗑"),
        types.KeyboardButton(text="Контакты 📞")
    ],
]
kbadm = [
    [
        types.KeyboardButton(text="Каталог 📕"),
        types.KeyboardButton(text="Корзина 🗑"),
        types.KeyboardButton(text="Контакты 📞")
    ],
]
kbadm1 = [
    [
        types.KeyboardButton(text="Каталог 📕"),
        types.KeyboardButton(text="Корзина 🗑"),
        types.KeyboardButton(text="Контакты 📞"),
    ],
    [
        types.KeyboardButton(text="Добавить товар 📥"),
        types.KeyboardButton(text="Добавить описание 📥"),
    ],
    [
        types.KeyboardButton(text="Удалить товар 📤"),
        types.KeyboardButton(text="Удалить описание 📤"),
    ],
    [
        types.KeyboardButton(text="Сделать рассылку 📫")
    ],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,

)

keyadm1 = types.ReplyKeyboardMarkup(
    keyboard=kbadm1,
    resize_keyboard=True,

)
canc = [
    [
        types.KeyboardButton(text="Отмена ❌", callback_data="cancel")

    ],
]
udk = [
    [
        types.KeyboardButton(text="Удалить из корзины ❌", callback_data="udl"),
        types.KeyboardButton(text="Оплатить 💵", callback_data="money")

    ],
    [
        types.KeyboardButton(text="Возврат 🔄", callback_data="vozv"),


    ],
]
udal = types.ReplyKeyboardMarkup(
    keyboard=udk,
    resize_keyboard=True,

)
cancel = types.ReplyKeyboardMarkup(
    keyboard=canc,
    resize_keyboard=True,

)


def ct():
    menu_list = [
        [InlineKeyboardButton(text="товар 1", callback_data="btn1")],
        [InlineKeyboardButton(text="товар 2", callback_data="btn2")],
        [InlineKeyboardButton(text="товар 3", callback_data="btn3")],

    ]
    return InlineKeyboardMarkup(inline_keyboard=menu_list)


def genmarkup(data):  # передаём в функцию data
    k = InlineKeyboardBuilder()
    for i in data:  # цикл для создания кнопок
        k.row(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}'))
        print(i[0])

    return k


def dob():  # передаём в функцию data
    k = InlineKeyboardBuilder()

    k.row(InlineKeyboardButton(text='Добавить в корзину', callback_data='dob'))

    return k
