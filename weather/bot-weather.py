import telegram
import requests
import json
import time
from datetime import datetime, timedelta
from pytz import timezone
import os
from prometheus_client import start_http_server, Counter, Gauge

# Задаем константы
TOKEN = os.environ.get('weather_TOKEN')
CHAT_ID = os.environ.get('weather_CHAT_ID')
API_KEY = os.environ.get('weather_API_KEY')
TIMEZONE = os.environ.get('weather_TIMEZONE')

# Задаем координаты города 1
weather_CITY_1_LAT = os.environ.get('weather_CITY_1_LAT')
weather_CITY_1_LON = os.environ.get('weather_CITY_1_LON')

# Задаем координаты города 2
weather_CITY_2_LAT = os.environ.get('weather_CITY_2_LAT')
weather_CITY_2_LON = os.environ.get('weather_CITY_2_LON')

# Создаем объект бота
bot = telegram.Bot(token=TOKEN)

# Функция отправки сообщения
def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

# Функция замены символа состояния погоды на соответствующие эмодзи
def get_weather_emoji(icon_code):
    weather_icons = {
        '01d': '☀️',  # ясно (день)
        '01n': '🌙',  # ясно (ночь)
        '02d': '🌤️',  # малооблачно (день)
        '02n': '☁️🌙',  # малооблачно (ночь)
        '03d': '☁️',  # облачно с прояснениями (день)
        '03n': '☁️',  # облачно с прояснениями (ночь)
        '04d': '☁️',  # облачно (день)
        '04n': '☁️',  # облачно (ночь)
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

# Функция получения прогноза погоды
def get_weather():
    try:
        url_1 = f'https://api.openweathermap.org/data/2.5/weather?lat={weather_CITY_1_LAT}&lon={weather_CITY_1_LON}&appid={API_KEY}&lang=ru&units=metric'
        response_1 = requests.get(url_1)
        data_1 = json.loads(response_1.text)
        description_1 = data_1['weather'][0]['description']
        description_1 = description_1.capitalize()
        icon_1 = data_1['weather'][0]['icon']
        icon_1 = get_weather_emoji(icon_1)
        temp_1 = data_1['main']['temp']
        feels_like_1 = data_1['main']['feels_like']
        wind_speed_1 = data_1['wind']['speed']
        humidity_1 = data_1['main']['humidity']

        url_2 = f'https://api.openweathermap.org/data/2.5/weather?lat={weather_CITY_2_LAT}&lon={weather_CITY_2_LON}&appid={API_KEY}&lang=ru&units=metric'
        response_2 = requests.get(url_2)
        data_2 = json.loads(response_2.text)
        description_2 = data_2['weather'][0]['description']
        description_2 = description_2.capitalize()
        icon_2 = data_2['weather'][0]['icon']
        icon_2 = get_weather_emoji(icon_2)
        temp_2 = data_2['main']['temp']
        feels_like_2 = data_2['main']['feels_like']
        wind_speed_2 = data_2['wind']['speed']
        humidity_2 = data_2['main']['humidity']

        return f'Погода на районе:\n\n{description_1} {icon_1}\nТемпература: {temp_1}°C\nОщущается как: {feels_like_1}°C\nВлажность {humidity_1}%\nСкорость ветра: {wind_speed_1} м/с\n\nПогода на даче:\n\n{description_2} {icon_2}\nТемпература: {temp_2}°C\nОщущается как: {feels_like_2}°C\nВлажность {humidity_2}%\nСкорость ветра: {wind_speed_2} м/с'
    except Exception as e:
        print(e)
        return 'Не удалось получить прогноз погоды'

# Функция проверки времени и отправки сообщения
def check_time_and_send():
    now = datetime.now(timezone(TIMEZONE))
    if now.hour == 7 and now.minute == 30:
        send_message(get_weather())
    elif now.hour == 13 and now.minute == 30:
        send_message(get_weather())
    elif now.hour == 17 and now.minute == 30:
        send_message(get_weather())
    elif now.hour == 20 and now.minute == 30:
        send_message(get_weather())
    elif now.hour == 3 and now.minute == 0:
        send_message(get_weather())

if os.environ.get('CI'):
    exit(0)

# Основной цикл программы
while True:
    start_http_server(57899)
    check_time_and_send()
    time.sleep(60) # Пауза в 60 секунд
