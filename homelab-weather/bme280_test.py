import logging
import sys
import time
import os
from smbus2 import SMBus
from bme280 import BME280
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import subprocess

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Снижение уровня логирования для библиотеки telegram
logging.getLogger("httpx").setLevel(logging.WARNING)

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

# Чтение данных с датчика
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
        "Я тут, чтобы держать тебя в курсе всех атмосферных дел — будь то солнечный день или внезапный ливень!\n"
        "Хочешь узнать, что творится за окном прямо сейчас? Введи /weather, и я выдам свежие данные о температуре, давлении и влажности. 🌡️💧📉\n"
        "Готов в любое время дня и ночи! Ну, почти. 😄"
    )

    await update.message.reply_text(welcome_message)
    logging.info("Команда /start получена. Приветственное сообщение отправлено пользователю.")

# Обработчик команды /weather для отправки текущей погоды
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем текущие данные с датчика
    weather_info = get_weather_data(bme280)
    # Отправляем сообщение с данными о погоде пользователю
    await update.message.reply_text(weather_info)
    logging.info("Команда /weather получена. Данные о погоде отправлены пользователю.")

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

    # Запускаем бота
    logging.info("Бот запущен и готов принимать команды.")
    application.run_polling()
