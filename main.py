import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, Я бот!')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Выбирете действие: \n /start \n /help ')

@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интелект - это интеллект, демонстрируемый машинами, в частности, компьютерными системами.')

@dp.message(F.photo )
async def aiphoto(message: Message):
    await message.answer('Ого какая фотка!')

@dp.message(Command('photo') )
async def photo(message: Message):
    await message.answer_photo(photo= 'https://static.tildacdn.com/tild3662-3738-4462-b738-333430386539/e362c0d0-1b30-490f-a.jpg', caption= 'Это картинка')

async def main():
    await dp.start_polling(bot)

if __name__== '__main__':
    asyncio.run(main())