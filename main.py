import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, FSInputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import utils
from handlers import router


@router.callback_query(F.data == "add_new_order")
async def add_new_order(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get('title'):
        await clbck.message.answer("Заполните название заказа!")
        return
    if not data.get('amount'):
        await clbck.message.answer("Заполните сумму заказа!")
        return    
    title = data['title']
    amount = int(data['amount'] * 100)

    await send_buy_query(clbck.message.chat.id, title, [LabeledPrice(label=title, amount=amount)])

@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@router.message(Command('buy'))
async def test(msg: Message):
    await send_buy_query(msg.chat.id, "проверОЧКА", [LabeledPrice(label='Плати давай', amount=10000)])

@router.message()
async def message_handler(msg: Message):
    print(msg.text)
    await msg.answer(f"Используйте /menu для взаимодействия")

async def send_buy_query(chat_id, title, prices):
    photo = FSInputFile('creo_logo.jpg')
    await bot.send_invoice(chat_id,
                           title=title,
                           description="Оплата заказа",
                           provider_token=config.PAYMENT_TOKEN,
                           currency="rub",
                           photo_url="https://downloader.disk.yandex.ru/preview/fc51d80ab9bbcefd22c44f2c29d636c3ed8ff185bf23af16e9f0f45c945a2bf8/65724c61/CT7fSOuhLp4fkouLX2ybj_nVEXnmya_AKe807xew9nWjMbT_A-L_o_NZstv04U1NxOB2qzWgCbCFa5uQOMSUlQ%3D%3D?uid=0&filename=creo_logo.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1850x963",
                           photo_width=250,
                           photo_height=250,
                           photo_size=250,
                           is_flexible=False,
                           prices=prices,
                           start_parameter="one-month-subscription",
                           payload=f"{title}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
