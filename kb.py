from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from callback_data import *

from db import ManageDB

import text


def get_profile_keyboard() -> InlineKeyboardMarkup:
    profile = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить данные", callback_data="set_profile_query"),
            InlineKeyboardButton(text=text.back_button_text, callback_data="show_menu")
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
    builder = InlineKeyboardBuilder()
    builder.button(text="Профиль", callback_data="show_profile")
    builder.button(text="Профиль художника", callback_data="show_contractor_profile")
    builder.button(text="Актуальные заказы", callback_data="show_order_list")
    builder.button(text="История заказов", callback_data="show_history_list")
    builder.adjust(1)
    return builder.as_markup()

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

async def get_orders_keyboard(tg_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Создать заказ", callback_data="new_order")
    builder.button(text=text.back_button_text, callback_data="show_menu")
    orders = await ManageDB().get_actual_orders(tg_id)
    for order in orders:
        builder.button(text=f"Информация о заказе {order['title']}", callback_data=f"info_order_{order['id']}_t")
    builder.adjust(1)
    return builder.as_markup()

async def get_history_keyboard(tg_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=text.back_button_text, callback_data="show_menu")
    orders = await ManageDB().get_history(tg_id)
    for order in orders:
        builder.button(text=f"Информация о заказе {order['title']}", callback_data=f"info_order_{order['id']}_f")
    builder.adjust(1)
    return builder.as_markup()

def get_new_order_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Название", callback_data="new_order_set_title")
    builder.button(text="Описание", callback_data="new_order_set_description")
    builder.button(text="Цена", callback_data="new_order_set_amount")
    builder.button(text="Опубликовать заказ", callback_data="add_new_order")
    builder.adjust(1)
    return builder.as_markup()

def get_info_order_keyboard(id, is_order : bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_order == 't':
        builder.button(text="Удалить", callback_data=f"delete_order_{id}")
        builder.button(text=text.back_button_text, callback_data=f"show_order_list")
    else:
        builder.button(text=text.back_button_text, callback_data=f"show_history_list")
    builder.adjust(1)
    return builder.as_markup()
