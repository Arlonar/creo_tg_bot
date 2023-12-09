from db import ManageDB
import text
from dadata import Dadata
from config import DADATA_API_KEY
from aiogram.types import User


async def register(tg_id):
    await ManageDB().create_user(tg_id)

async def check_can_register_contractor(tg_id):
    res = await ManageDB().get_profile_info(tg_id)
    return res['first_name'] and res['last_name']

async def get_profile(tg_id):
    res = await ManageDB().get_profile_info(tg_id)
    data = f"<b>Имя:</b> {res['first_name'] if res['first_name'] != None else text.no_profile_data}\n" +\
        f"<b>Фамилия:</b> {res['last_name'] if res['last_name'] != None else text.no_profile_data}\n" +\
        f"<b>Пол:</b> {res['gender'] if res['gender'] != None else text.no_profile_data}\n" +\
        f"<b>Почта:</b> {res['email'] if res['email'] != None else text.no_profile_data}\n" +\
        f"<b>Адрес доставки:</b> {res['address'] if res['address'] != None else text.no_profile_data}\n" +\
        f"<b>Номер телефона:</b> {res['phone'] if res['phone'] != None else text.no_profile_data}"
    return data

async def check_is_contractor(tg_id):
    res = await ManageDB().get_profile_info(tg_id)
    return res['is_contractor']

async def set_profile(tg_id, first_name=None, last_name=None, gender=None, email=None, address=None, phone=None):
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'email': email,
        'address': address,
        'phone': phone
        }
    await ManageDB().set_profile_info(tg_id, data)

def get_address_from_coords(latitude, longitude):
    return Dadata(DADATA_API_KEY).geolocate(name="address", lat=latitude, lon=longitude),

async def get_contractor_info(tg_id):
    res = await ManageDB().get_contractor_info(tg_id)
    data = f"Пока здесь больше ничего нет :)\n" +\
        f"Имя: <b>{res['first_name']}</b>\n" +\
        f"Фамилия: <b>{res['last_name']}</b>"
    return data

async def get_contractors():
    res = await ManageDB().get_notify_contractors_ids()
    return res

async def register_contractor(tg_id):
    await ManageDB().register_contractor(tg_id)

async def get_orders(tg_id,):
    res = await ManageDB().get_actual_orders(tg_id)
    if not res:
        return "У вас пока нет заказов"
    data = "<b>Текущие заказы:</b>\n\n"
    for ind, elem in enumerate(res):
        if elem['status'] == 'in_progress':
            contractor = f'<a href="tg://user?id={elem["tg_id"]}">{elem["first_name"]} {elem["last_name"]}</a>'
        else:
            contractor = "отсутствует"
        data += f"{ind + 1}) Заказ <b>{elem['title']}</b> стоимостью <i>{float(elem['amount'])} RUB</i>.\n" +\
                f"Исполнитель: <i>{contractor}\n\n</i>"
    return data

async def get_history(tg_id):
    res = await ManageDB().get_history(tg_id)
    data = "<b>История заказов:</b>\n\n"
    if not res:
        return 'Вы еще ничего не заказывали, либо заказы не незаврешены'
    for ind, elem in enumerate(res):
        data += f"{ind + 1}) Заказ <b>{elem['title']}</b> {'завершен' if elem['status'] == 'done' else 'отменен'}\n"
    return data

async def get_order(order_id):
    res = await ManageDB().get_order_by_id(order_id)
    match res['status']:
        case 'canceled':
            status = 'отменен'
            contractor = "отсутствует"
        case 'waiting':
            status = 'в ожидании художника'
            contractor = "отсутствует"
        case 'in_progress':
            status = 'художник делает'
            contractor = f'<a href="tg://user?id={res["tg_id"]}">{res["first_name"]} {res["last_name"]}</a>'
        case 'done':
            status = 'завершен'
            contractor = f'<a href="tg://user?id={res["tg_id"]}">{res["first_name"]} {res["last_name"]}</a>'
    data = f"Заказ <b>{res['title']}</b>\n\nОписание заказа: <i>{res['description']}</i>\n\nСумма заказа: <i>{float(res['amount'])} RUB</i>\n\n" +\
        f"Исполнитель: <i>{contractor}</i>\n\nСтатус заказа: <i>{status}</i>"
    return data

async def add_order(tg_id, amount, title, description):
    await ManageDB().add_order(tg_id, amount, title, description)

async def delete_order(order_id) -> bool:
    db = ManageDB()
    order_info = await db.get_order_by_id(order_id)
    if order_info['tg_id']:
        return False
    await db.delete_order(order_id)
    return True
