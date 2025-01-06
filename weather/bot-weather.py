import os
import json
import requests
import logging
import asyncio
from datetime import datetime
from pytz import timezone

# Библиотеки Prometheus и telegram
from prometheus_client import start_http_server
import telegram

# ==========================
# Настройка логирования
# ==========================
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Скрываем детальные логи telegram / httpx, чтобы не утекал токен
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.vendor.ptb_urllib3.urllib3.connectionpool').setLevel(logging.WARNING)

# ==========================
# Переменные окружения
# ==========================
TOKEN   = os.environ.get('weather_TOKEN')
CHAT_ID = os.environ.get('weather_CHAT_ID')
API_KEY = os.environ.get('weather_API_KEY')
TIMEZONE_NAME = os.environ.get('weather_TIMEZONE')

CITY_1_LAT = os.environ.get('weather_CITY_1_LAT')
CITY_1_LON = os.environ.get('weather_CITY_1_LON')
CITY_2_LAT = os.environ.get('weather_CITY_2_LAT')
CITY_2_LON = os.environ.get('weather_CITY_2_LON')

# ==========================
# Создаём бота
# ==========================
bot = telegram.Bot(token=TOKEN)

# ==========================
# Эмодзи для иконок погоды
# ==========================
def get_weather_emoji(icon_code: str) -> str:
    weather_icons = {
        '01d': '☀️',   # ясно (день)
        '01n': '🌙',   # ясно (ночь)
        '02d': '🌤️',  # малооблачно (день)
        '02n': '☁️🌙', # малооблачно (ночь)
        '03d': '☁️',   # облачно с прояснениями (день)
        '03n': '☁️',   # облачно с прояснениями (ночь)
        '04d': '☁️',   # облачно (день)
        '04n': '☁️',   # облачно (ночь)
        '09d': '🌧️',  # дождь (день)
        '09n': '🌧️',  # дождь (ночь)
        '10d': '🌦️',  # дождь с прояснениями (день)
        '10n': '🌦️',  # дождь с прояснениями (ночь)
        '11d': '⛈️',  # гроза (день)
        '11n': '⛈️',  # гроза (ночь)
        '13d': '❄️',  # снег (день)
        '13n': '❄️',  # снег (ночь)
        '50d': '🌫️',  # туман (день)
        '50n': '🌫️',  # туман (ночь)
    }
    return weather_icons.get(icon_code, '')

# ==========================
# Получение погоды (синхронно)
# ==========================
def get_weather() -> str:
    """
    Возвращает детализированное сообщение о погоде:
    - "Погода на районе" (CITY_1_LAT/LON)
    - "Погода на даче"   (CITY_2_LAT/LON)
    """
    try:
        # ---- Город 1 ----
        url_1 = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={CITY_1_LAT}&lon={CITY_1_LON}&appid={API_KEY}&lang=ru&units=metric"
        )
        response_1 = requests.get(url_1)
        data_1 = json.loads(response_1.text)

        description_1 = data_1['weather'][0]['description'].capitalize()
        icon_1 = get_weather_emoji(data_1['weather'][0]['icon'])
        temp_1 = data_1['main']['temp']
        feels_like_1 = data_1['main']['feels_like']
        wind_speed_1 = data_1['wind']['speed']
        humidity_1 = data_1['main']['humidity']

        # ---- Город 2 ----
        url_2 = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={CITY_2_LAT}&lon={CITY_2_LON}&appid={API_KEY}&lang=ru&units=metric"
        )
        response_2 = requests.get(url_2)
        data_2 = json.loads(response_2.text)

        description_2 = data_2['weather'][0]['description'].capitalize()
        icon_2 = get_weather_emoji(data_2['weather'][0]['icon'])
        temp_2 = data_2['main']['temp']
        feels_like_2 = data_2['main']['feels_like']
        wind_speed_2 = data_2['wind']['speed']
        humidity_2 = data_2['main']['humidity']

        message = (
            f"Погода на районе:\n\n"
            f"{description_1} {icon_1}\n"
            f"Температура: {temp_1}°C\n"
            f"Ощущается как: {feels_like_1}°C\n"
            f"Влажность {humidity_1}%\n"
            f"Скорость ветра: {wind_speed_1} м/с\n\n"
            f"Погода на даче:\n\n"
            f"{description_2} {icon_2}\n"
            f"Температура: {temp_2}°C\n"
            f"Ощущается как: {feels_like_2}°C\n"
            f"Влажность {humidity_2}%\n"
            f"Скорость ветра: {wind_speed_2} м/с"
        )
        return message

    except Exception as e:
        logger.error(f"Не удалось получить прогноз погоды: {e}")
        return "Не удалось получить прогноз погоды"

# ==========================
# Асинхронная отправка сообщения
# ==========================
async def send_message(text: str) -> None:
    """
    Асинхронно отправляет сообщение в Telegram-чат
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
        logger.info("Сообщение отправлено")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

# ==========================
# Асинхронная проверка времени
# ==========================
async def check_time_and_send() -> None:
    """
    Проверяет текущее время в заданном часовом поясе
    и отправляет сообщение в Telegram, если совпадает с нужным временем:
    03:00, 07:30, 13:30, 17:30, 20:30
    """
    now = datetime.now(timezone(TIMEZONE_NAME))
    current_hour = now.hour
    current_minute = now.minute

    # Список нужных пар (часы, минуты)
    scheduled_times = [
        (3, 0),
        (7, 30),
        (13, 30),
        (17, 30),
        (20, 30),
    ]

    if (current_hour, current_minute) in scheduled_times:
        weather_info = get_weather()  # Синхронное получение погоды
        await send_message(weather_info)

# ==========================
# Основной асинхронный цикл
# ==========================
async def main():
    """
    Запускает HTTP-сервер Prometheus для метрик на порту 57899,
    и затем каждую минуту проверяет время и при необходимости
    отправляет сообщение в Telegram.
    """
    from prometheus_client import start_http_server
    logging.info('Start http server')
    start_http_server(57899)  # Запускаем Prometheus на одном порту один раз

    while True:
        await check_time_and_send()
        await asyncio.sleep(60)  # Асинхронная пауза в 60 секунд

# ==========================
# Точка входа
# ==========================
if __name__ == "__main__":
    logging.info('Start bot polling')
    asyncio.run(main())

