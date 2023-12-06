import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
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

@router.message()
async def message_handler(msg: Message):
    print(msg.text)
    await msg.answer(f"Используйте /menu для взаимодействия")

async def send_buy_query(chat_id, title, prices):
    await bot.send_invoice(chat_id,
                           title=title,
                           description="Оплата заказа",
                           provider_token=config.PAYMENT_TOKEN,
                           currency="rub",
                           photo_url="https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?q=80&w=1965&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                           photo_width=570,
                           photo_height=713,
                           photo_size=713,
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
