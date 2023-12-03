from db import ManageDB
import text
from dadata import Dadata
from config import DADATA_API_KEY


async def register(tg_id):
    await ManageDB().create_user(tg_id)

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
