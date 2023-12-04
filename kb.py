from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from callback_data import *


def get_profile_keyboard() -> InlineKeyboardMarkup:
    profile = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить данные", callback_data="set_profile_query"),
            InlineKeyboardButton(text="Вернуться в меню", callback_data="show_menu")
        ]
    ])
    return profile


def get_change_profile_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Имя", callback_data="change_profile_first_name")
    builder.button(text="Фамилия", callback_data="change_profile_last_name")
    builder.button(text="Пол", callback_data="change_profile_gender")
    builder.button(text="Почта", callback_data="change_profile_email")
    builder.button(text="Адрес доставки", callback_data="change_profile_address")
    builder.button(text="Телефон", callback_data="change_profile_phone")
    builder.adjust(2)
    return builder.as_markup()

def get_menu_keyboard() -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Профиль", callback_data="show_profile"),
            InlineKeyboardButton(text="Профиль художника", callback_data="show_contractor_profile"),
            InlineKeyboardButton(text="Список заказов", callback_data="show_order_list")
        ]
    ])
    return menu

def get_change_gender_keyboard() -> ReplyKeyboardMarkup:
    gender = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Мужской"),
            KeyboardButton(text="Женcкий")
        ]
    ], resize_keyboard=True, input_field_placeholder="Выберите пол")
    return gender

def get_share_location_keyboard() -> ReplyKeyboardMarkup:
     return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поделиться местоположением", request_location=True)]],
                                 resize_keyboard=True, input_field_placeholder="Введите адрес доставки")

def get_yes_no_contractor_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="register_contractor"),
            InlineKeyboardButton(text="Нет", callback_data="show_menu")
        ]
    ])

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
