from smbus2 import SMBus
from bme280 import BME280
import subprocess
import sys
import time

# Функция для проверки устройства по адресу 0x76
def check_device_address(address=0x76):
    try:
        # Запускаем команду i2cdetect и ищем адрес
        result = subprocess.run(["i2cdetect", "-y", "1"], capture_output=True, text=True)
        if f"{address:02x}" not in result.stdout:
            print(f"Ошибка: устройство по адресу 0x{address:02x} не найдено. Проверьте подключение.")
            return False
        return True
    except Exception as e:
        print(f"Ошибка при проверке устройства: {e}")
        return False

# Инициализация датчика
def initialize_sensor():
    try:
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        return bme280
    except Exception as e:
        print(f"Ошибка при инициализации датчика: {e}")
        return None

# Чтение и вывод данных
def read_sensor_data(bme280):
    try:
        # Принудительная задержка для стабилизации показаний
        time.sleep(1)
        bme280.update_sensor()  # Первое обновление данных
        time.sleep(0.5)  # Дополнительная задержка
        bme280.update_sensor()  # Второе обновление данных для актуальности
        
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        
        print(f"Температура: {temperature:.2f} °C")
        print(f"Давление: {pressure:.2f} hPa")
        print(f"Влажность: {humidity:.2f} %")
    except Exception as e:
        print(f"Ошибка при чтении данных с датчика: {e}")

# Основная программа
if __name__ == "__main__":
    # Шаг 1: Проверка устройства
    if not check_device_address():
        sys.exit(1)  # Выход, если устройство не найдено

    # Шаг 2: Инициализация датчика
    bme280 = initialize_sensor()
    if bme280 is None:
        sys.exit(1)  # Выход, если инициализация не удалась

    # Шаг 3: Чтение данных
    read_sensor_data(bme280)
