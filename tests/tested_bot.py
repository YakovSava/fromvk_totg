from asyncio import run
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import Command

with open("tested_token.txt", "r", encoding="utf-8") as file:
    bot = Bot(token=file.read())
dp = Dispatcher()

@dp.message(Command("start"))
async def start_reg(message: Message):
    await message.answer("Напишите сообщение которое будет отправлено в канал!")
        
@dp.message()
async def echo_channel(message:Message):
    await message.answer("Проверьте канал!")
    await bot.send_message(chat_id=-1001527506224, text=message.text)
	
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)
	
if __name__ == "__main__":
    run(main())