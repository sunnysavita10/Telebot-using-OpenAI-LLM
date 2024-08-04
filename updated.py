import asyncio
import logging
from aiogram import Bot, Dispatcher, types

TOKEN = "insert token"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message_handler()
    async def echo_message(msg: types.Message):
        await msg.answer(msg.text)

    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())