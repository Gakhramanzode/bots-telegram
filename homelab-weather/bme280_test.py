import logging
from smbus2 import SMBus
from bme280 import BME280
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from prometheus_client import Gauge, Counter, start_http_server
import subprocess
import sys
import time
import os

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Снижение уровня логирования для библиотеки telegram
logging.getLogger("httpx").setLevel(logging.WARNING)

# Настраиваем метрики Prometheus
TEMPERATURE_GAUGE = Gauge("meteo_temperature", "Current temperature in Celsius")
PRESSURE_GAUGE = Gauge("meteo_pressure", "Current atmospheric pressure in hPa")
HUMIDITY_GAUGE = Gauge("meteo_humidity", "Current humidity percentage")
BOT_START_COUNTER = Counter("bot_start_requests", "Count of /start command requests")
BOT_WEATHER_COUNTER = Counter("bot_weather_requests", "Count of /weather command requests")

# Функция для проверки устройства по адресу 0x76
def check_device_address(address=0x76):
    try:
        result = subprocess.run(["i2cdetect", "-y", "1"], capture_output=True, text=True)
        if f"{address:02x}" not in result.stdout:
            logging.error(f"Устройство по адресу 0x{address:02x} не найдено. Проверьте подключение.")
            return False
        logging.info(f"Устройство по адресу 0x{address:02x} найдено.")
        return True
    except Exception as e:
        logging.error(f"Ошибка при проверке устройства: {e}")
        return False

# Инициализация датчика
def initialize_sensor():
    try:
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        logging.info("Датчик BME280 успешно инициализирован.")
        return bme280
    except Exception as e:
        logging.error(f"Ошибка при инициализации датчика: {e}")
        return None

# Чтение данных с датчика и обновление метрик
def get_weather_data(bme280):
    try:
        # Принудительная задержка для стабилизации показаний
        time.sleep(1)
        bme280.update_sensor()
        time.sleep(0.5)
        bme280.update_sensor()

        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()

        # Обновляем метрики Prometheus
        TEMPERATURE_GAUGE.set(temperature)
        PRESSURE_GAUGE.set(pressure)
        HUMIDITY_GAUGE.set(humidity)

        # Формируем строку с данными
        weather_info = (
            f"Температура: {temperature:.2f} °C\n"
            f"Давление: {pressure:.2f} hPa\n"
            f"Влажность: {humidity:.2f} %"
        )
        return weather_info
    except Exception as e:
        logging.error(f"Ошибка при чтении данных с датчика: {e}")
        return "Ошибка при получении данных о погоде."

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        f"Привет, {update.effective_user.first_name}! Я — твой личный погодный эксперт, 'Cloudy with a Chance'. 🌦️\n"
        "Я тут, чтобы держать тебя в курсе всех атмосферных дел!\n"
        "Хочешь узнать, что творится за окном? Введи /weather, и я покажу свежие данные. 🌡️💧📉"
    )

    await update.message.reply_text(welcome_message)
    logging.info("Команда /start получена. Приветственное сообщение отправлено пользователю.")
    BOT_START_COUNTER.inc()  # Увеличиваем счётчик запросов к /start

# Обработчик команды /weather для отправки текущей погоды
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    weather_info = get_weather_data(bme280)
    await update.message.reply_text(weather_info)
    logging.info("Команда /weather получена. Данные о погоде отправлены пользователю.")
    BOT_WEATHER_COUNTER.inc()  # Увеличиваем счётчик запросов к /weather

# Основная программа
if __name__ == "__main__":
    # Шаг 1: Проверка устройства
    if not check_device_address():
        sys.exit(1)

    # Шаг 2: Инициализация датчика
    bme280 = initialize_sensor()
    if bme280 is None:
        sys.exit(1)

    # Шаг 3: Инициализация Telegram бота
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Токен Telegram бота не найден. Установите TELEGRAM_BOT_TOKEN в переменные окружения.")
        sys.exit(1)

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    # Запуск HTTP-сервера Prometheus для экспорта метрик
    start_http_server(51676)  # Порт 51676 для метрик Prometheus
    logging.info("Prometheus HTTP-сервер для метрик запущен на порту 51676")

    # Запускаем бота в фоновом режиме
    application.run_polling()

    # Шаг 4: Бесконечный цикл для периодического считывания данных
    while True:
        get_weather_data(bme280)
        time.sleep(600)  # Интервал в 10 минут
