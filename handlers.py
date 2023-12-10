from aiogram import Router, F, types, flags, html
from aiogram.methods.send_invoice import SendInvoice
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, LabeledPrice
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import Command

from states import Gen
from callback_data import ChangeProfile
import utils
import kb
import text
import config


router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=html.bold(html.quote(msg.from_user.full_name))), reply_markup=kb.get_menu_keyboard())
    await utils.register(msg.from_user.id)

@router.callback_query(F.data == "show_contractor_profile")
async def show_contractor_profile_query(clbck:CallbackQuery, state: FSMContext):
    constractor = await utils.check_is_contractor(clbck.from_user.id)
    if not constractor:
        await clbck.message.answer(text.no_contractor_message, reply_markup=kb.get_yes_no_contractor_keyboard())
        await clbck.answer()
        return 
    info = await utils.get_contractor_info(clbck.from_user.id)
    await clbck.message.answer(info)
    await clbck.answer()

@router.callback_query(F.data == "register_contractor")
async def register_contractor_query(clbck: CallbackQuery, state: FSMContext):
    can = await utils.check_can_register_contractor(clbck.from_user.id)
    if can:
        await utils.register_contractor(clbck.from_user.id)
        await clbck.message.answer("Учетная запись создана")
    else:
        await clbck.message.answer("Сначала заполните профиль!")
    await clbck.answer()

@router.callback_query(F.data == "show_contractor_profile")
async def show_contractor_profile_query(clbck: CallbackQuery, state: FSMContext):
    info = await utils.get_contractor_info(clbck.from_user.id)
    clbck.message.answer(info)

@router.callback_query(F.data == "show_profile")
async def show_profile_query(clbck: CallbackQuery, state: FSMContext):
    data = await utils.get_profile(clbck.from_user.id)
    if not data:
        data = "Используйте /start"
    await clbck.message.answer(data, reply_markup=kb.get_profile_keyboard())
    await clbck.answer()

@router.callback_query(F.data == 'show_order_list')
async def show_order_list_query(clbck: CallbackQuery, state: FSMContext):
    keyboard = await kb.get_orders_keyboard(clbck.from_user.id)
    data = await utils.get_orders(clbck.from_user.id)
    await clbck.message.answer(data, reply_markup=keyboard)
    await clbck.answer()

@router.callback_query(F.data == 'show_history_list')
async def show_history_list(clbck: CallbackQuery, state: FSMContext):
    keyboard = await kb.get_history_keyboard(clbck.from_user.id)
    data = await utils.get_history(clbck.from_user.id)
    await clbck.message.answer(data, reply_markup=keyboard)
    await clbck.answer()

@router.callback_query(F.data == 'set_profile_query')
async def change_profile_query(clbck: CallbackQuery):
    await clbck.message.answer('Выберите данные, которые хотите изменить', reply_markup=kb.get_change_profile_keyboard())
    await clbck.answer()

@router.callback_query(F.data.startswith("change_profile_"))
async def change_profile_data(clbck: CallbackQuery, state: FSMContext):
    match clbck.data:
        case "change_profile_first_name":
            await clbck.message.answer("Введите имя")
            await state.set_state(Gen.profile_set_first_name)
        case "change_profile_last_name":
            await clbck.message.answer("Введите фамилию")
            await state.set_state(Gen.profile_set_last_name)
        case "change_profile_gender":
            await clbck.message.answer("Выберите пол", reply_markup=kb.get_change_gender_keyboard())
            await state.set_state(Gen.profile_set_gender)
        case "change_profile_email":
            await clbck.message.answer("Введите email")
            await state.set_state(Gen.profile_set_email)
        case "change_profile_address":
            await clbck.message.answer("Введите адрес доставки", reply_markup=kb.get_share_location_keyboard())
            await state.set_state(Gen.profile_set_address)
        case "change_profile_phone":
            await clbck.message.answer("Введите номер телефона")
            await state.set_state(Gen.profile_set_phone)
    await clbck.answer()

@router.message(Gen.profile_set_first_name)
async def set_first_name_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, first_name=msg.text)
    await msg.answer(f'Имя изменено на {msg.text}')
    await state.clear()

@router.message(Gen.profile_set_last_name)
async def set_last_name_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, last_name=msg.text)
    await msg.answer(f'Фамилия изменена на {msg.text}')
    await state.clear()

@router.message(Gen.profile_set_gender)
async def set_gender_state(msg: Message, state: FSMContext):
    if msg.text.lower() != 'мужской' and msg.text.lower() != 'женcкий':
        msg.answer(f'Выберите из списка!')
        return
    await utils.set_profile(msg.from_user.id, gender=msg.text)
    await msg.answer(f'Пол изменен на {msg.text}', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(Gen.profile_set_email)
async def set_email_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, email=msg.text)
    await msg.answer(f'Email изменен на {msg.text}')
    await state.clear()

@router.message(Gen.profile_set_address)
async def set_address_state(msg: Message, state: FSMContext):
    if msg.location:
        addr = utils.get_address_from_coords(msg.location.latitude, msg.location.longitude)[0][0]['value']
    else:
        addr = msg.text
    await utils.set_profile(msg.from_user.id, address=addr)
    await msg.answer(f'Адрес доставки изменен на {addr}', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(Gen.profile_set_phone)
async def set_phone_state(msg: Message, state: FSMContext):
    await utils.set_profile(msg.from_user.id, phone=msg.text)
    await msg.answer(f'Номер телефона изменен на {msg.text}')
    await state.clear()


@router.callback_query(F.data == "show_menu")
async def show_menu_query(clbck: CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.get_menu_keyboard())
    await clbck.answer()

@router.message(Command("menu"))
async def show_menu_command(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.get_menu_keyboard())


@router.callback_query(F.data == "new_order")
async def create_order_query(clbck: CallbackQuery):
    await clbck.message.answer(text=text.new_order, reply_markup=kb.get_new_order_keyboard())
    await clbck.answer()

@router.callback_query(F.data.startswith("new_order_set_"))
async def new_order_set_query(clbck: CallbackQuery, state: FSMContext):
    match clbck.data:
        case "new_order_set_title":
            await state.set_state(Gen.order_set_title)
            await clbck.message.answer(text="Напишите название заказа")
        case "new_order_set_description":
            await state.set_state(Gen.order_set_description)
            await clbck.message.answer(text="Напишите описание заказа")
        case "new_order_set_amount":
            await state.set_state(Gen.order_set_amount)
            await clbck.message.answer(text="Напишите цену заказа")
    await clbck.answer()

@router.message(Gen.order_set_title)
async def new_order_set_title_query(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer(f'Название изменено на: {msg.text}')
    await state.set_state(state=None)

@router.message(Gen.order_set_description)
async def new_order_set_description_query(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer(f'Описание изменено на: {msg.text}')
    await state.set_state(state=None)

@router.message(Gen.order_set_amount)
async def new_order_set_amount_query(msg: Message, state: FSMContext):
    await state.update_data(amount=float(msg.text))
    await msg.answer(f'Цена изменена на: {msg.text} RUB')
    await state.set_state(state=None)

@router.callback_query(F.data.startswith("info_order_"))
async def info_order_query(clbck: CallbackQuery):
    order_id, is_order = clbck.data.split('_')[2:]
    data = await utils.get_order(order_id)
    await clbck.message.answer(data, reply_markup=kb.get_info_order_keyboard(order_id, is_order))
    await clbck.answer()

@router.callback_query(F.data.startswith("delete_order_"))
async def delete_order_query(clbck: CallbackQuery):
    id = clbck.data.split('_')[2]
    success = await utils.delete_order(id)
    if not success:
        await clbck.message.answer(text.cant_delete_order)
        await clbck.answer()
        return
    await clbck.message.answer(text.success_delete_order)
    await clbck.answer()

@router.callback_query(F.data.startswith("respond_order_"))
async def respond_order_query(clbck: CallbackQuery):
    id = clbck.data.split('_')[2]
    await utils.set_contractor_for_order(id, clbck.from_user.id)
    await clbck.message.answer('Вы взялись за этот заказ!')
    await clbck.answer()
    # Сделать уведомление клиенту о том, что откликнулся художник








'''@router.message(Gen.profile)
@flags.chat_action("typing")
async def test(msg: Message, state: FSMContext):
    await msg.answer("YESyesYESyesYESyes")
    await state.clear()'''

