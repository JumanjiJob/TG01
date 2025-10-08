import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_weather():
    # Используйте HTTPS вместо HTTP
    city = "Aktobe"
    country = "KZ"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    # Установите таймаут для запроса
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as response:
                # Обрабатываем разные статус-коды
                if response.status == 200:
                    data = await response.json()

                    temperature = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    pressure = data['main']['pressure']
                    wind_speed = data['wind']['speed']
                    description = data['weather'][0]['description']
                    city_name = data['name']

                    weather_info = (
                        f"🌤 Погода в {city_name}:\n"
                        f"📝 {description.capitalize()}\n"
                        f"🌡 Температура: {temperature}°C\n"
                        f"💭 Ощущается как: {feels_like}°C\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"📊 Давление: {pressure} гПа\n"
                        f"💨 Скорость ветра: {wind_speed} м/с\n"
                        f"🕐 Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
                    )
                    return weather_info
                elif response.status == 401:
                    return "❌ Ошибка: Неверный API-ключ. Проверьте ключ в config.py"
                elif response.status == 404:
                    return "❌ Ошибка: Город не найден."
                else:
                    return f"❌ Ошибка API. Код: {response.status}"

        except aiohttp.ClientConnectorError:
            return "❌ Ошибка подключения к интернету"
        except asyncio.TimeoutError:
            return "❌ Превышено время ожидания ответа от сервера"
        except Exception as e:
            return f"❌ Неизвестная ошибка: {str(e)}"


# ... остальная часть кода (обработчики сообщений) остается без изменений


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот! Используй /weather для получения погоды в Актобе')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Выберите действие: \n/start \n/help \n/weather')


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект - это интеллект, демонстрируемый машинами, в частности, компьютерными системами.')


@dp.message(F.photo)
async def aiphoto(message: Message):
    await message.answer('Ого какая фотка!')


@dp.message(Command('photo'))
async def photo(message: Message):
    await message.answer_photo(
        photo='https://static.tildacdn.com/tild3662-3738-4462-b738-333430386539/e362c0d0-1b30-490f-a.jpg',
        caption='Это картинка')


# Обработчик команды /weather
@dp.message(Command('weather'))
async def weather_command(message: Message):
    await message.answer("⏳ Загружаю данные о погоде...")
    weather_info = await get_weather()
    await message.answer(weather_info)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())