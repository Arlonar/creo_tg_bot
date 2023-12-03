from aiogram import Router, F, types, flags, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import Command

from states import Gen
from callback_data import ChangeProfile
import utils
import kb
import text


router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=html.bold(html.quote(msg.from_user.full_name))), reply_markup=kb.get_menu_keyboard())
    await utils.register(msg.from_user.id)

@router.callback_query(F.data == "show_contractor_profile")
async def show_contractor_profile_query(clbck:CallbackQuery, state: FSMContext):
    constractor = await utils.check_is_contractor(clbck.from_user.id)
    if not constractor:
        await clbck.answer(text.no_contractor_message)
        return
    await clbck.answer('test')

@router.callback_query(F.data == "show_profile")
async def show_profile_query(clbck: CallbackQuery, state: FSMContext):
    data = await utils.get_profile(clbck.from_user.id)
    if not data:
        data = "Используйте /start"
    await clbck.message.answer(data, reply_markup=kb.get_profile_keyboard())

@router.callback_query(F.data == 'set_profile_query')
async def change_profile_query(clbck: CallbackQuery):
    await clbck.message.answer('Выберите данные, которые хотите изменить', reply_markup=kb.get_change_profile_keyboard())
    await clbck.answer()

@router.callback_query(F.data.startswith("change_profile_"))
async def change_profile_data(clbck: CallbackQuery, state: FSMContext):
    match clbck.data:
        case "change_profile_first_name":
            await clbck.message.answer("Введите имя")
            await state.set_state(Gen.set_first_name)
        case "change_profile_last_name":
            await clbck.message.answer("Введите фамилию")
            await state.set_state(Gen.set_last_name)
        case "change_profile_gender":
            await clbck.message.answer("Выберите пол", reply_markup=kb.get_change_gender_keyboard())
            await state.set_state(Gen.set_gender)
        case "change_profile_email":
            await clbck.message.answer("Введите email")
            await state.set_state(Gen.set_email)
        case "change_profile_address":
            await clbck.message.answer("Введите адрес доставки", reply_markup=kb.get_share_location_keyboard())
            await state.set_state(Gen.set_address)
        case "change_profile_phone":
            await clbck.message.answer("Введите номер телефона")
            await state.set_state(Gen.set_phone)
    clbck.answer()

@router.message(Gen.set_first_name)
async def set_first_name_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, first_name=msg.text)
    await msg.answer(f'Имя изменено на {msg.text}')
    await state.clear()

@router.message(Gen.set_last_name)
async def set_last_name_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, last_name=msg.text)
    await msg.answer(f'Фамилия изменена на {msg.text}')
    await state.clear()

@router.message(Gen.set_gender)
async def set_gender_state(msg: Message, state: FSMContext):
    if msg.text.lower() != 'мужской' and msg.text.lower() != 'женcкий':
        msg.answer(f'Выберите из списка!')
        return
    await utils.set_profile(msg.from_user.id, gender=msg.text)
    await msg.answer(f'Пол изменен на {msg.text}', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(Gen.set_email)
async def set_email_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, email=msg.text)
    await msg.answer(f'Email изменен на {msg.text}')
    await state.clear()

@router.message(Gen.set_address)
async def set_address_state(msg: Message, state: FSMContext):
    addr = utils.get_address_from_coords(msg.location.latitude, msg.location.longitude)[0][0]['value']
    await utils.set_profile(msg.from_user.id, address=addr)
    await msg.answer(f'Адрес доставки изменен на {addr}', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(Gen.set_phone)
async def set_phone_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, phone=msg.text)
    await msg.answer(f'Номер телефона изменен на {msg.text}')
    await state.clear()


@router.callback_query(F.data == "show_menu")
async def menu(clbck: CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.get_menu_keyboard())









'''@router.message(Gen.profile)
@flags.chat_action("typing")
async def test(msg: Message, state: FSMContext):
    await msg.answer("YESyesYESyesYESyes")
    await state.clear()'''



@router.message()
async def message_handler(msg: Message):
    print(msg.from_user.id)
    await msg.answer(f"Неизвестная команда.\nИспользуйте /help для просмотра списка команд.")

