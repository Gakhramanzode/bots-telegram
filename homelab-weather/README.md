# Cloudy with a Chance - Homelab Weather Bot 🌦️

Добро пожаловать! В этом проекте мы создадим простую погодную станцию с использованием микрокомпьютера Raspberry Pi Zero 2 W и датчика температуры, давления и влажности GY-BME280. А ещё этот бот будет отправлять данные о погоде через Telegram!

## Схема
![image](https://github.com/user-attachments/assets/56bd5792-04dd-48db-b623-e2fee9c1a9b6)

## Что потребуется?

1.	Микрокомпьютер Raspberry Pi Zero 2 W (или другой Raspberry Pi с поддержкой Wi-Fi).
2.	Датчик GY-BME280 (датчик температуры, давления и влажности).
3.	Соединительные провода Dupont для подключения датчика к Raspberry Pi.
4.	Карта памяти microSD (класс скорости U1 или выше) с операционной системой Raspberry Pi OS.
5.	Аккаунт в Telegram для создания бота и получения токена.

### Подключение датчика к Raspberry Pi

1.	Подключите датчик BME280 к Raspberry Pi с помощью проводов Dupont:
- VCC на датчике к 3.3V на Raspberry Pi (НЕ подключайте к 5V).
- GND на датчике к GND на Raspberry Pi.
- SCL на датчике к GPIO 3 (SCL) на Raspberry Pi.
- SDA на датчике к GPIO 2 (SDA) на Raspberry Pi.

> [!TIP]
> Мне помог вот этот сайт https://pinouts.vercel.app/board/raspberry-pi-zero-2-w

2. Убедитесь, что I2C включен на Raspberry Pi. Откройте raspi-config командой:
```bash
sudo raspi-config
```
Перейдите в Interface Options и включите I2C. Это позволит Raspberry Pi взаимодействовать с датчиком через I2C.

4.	Откройте терминал и проверьте подключение датчика с помощью команды:
```bash
i2cdetect -y 1
```
Если видите `0x76` в выводе, значит, датчик подключён правильно. Пример:
```bash
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
```

### Установка ПО и запуск проекта

Шаг 1: Подготовка кода

1.	Скачайте и установите необходимые библиотеки, указанные в файле `requirements.txt`.
2.	Установите токен вашего Telegram бота в переменной окружения `TELEGRAM_BOT_TOKEN`.

Шаг 2: Сборка Docker-образа

1.	Откройте терминал и выполните команды:
```bash
git clone git@github.com:Gakhramanzode/bots-telegram.git
cd bots-telegram/homelab-weather/
sudo docker build -t weather-bot:v0.0.1 .
```
Шаг 3: Запуск Docker-контейнера

1.	Запустите контейнер с помощью команды:
```bash
sudo docker run -d --name weather-bot-container --device /dev/i2c-1 -e TELEGRAM_BOT_TOKEN=токен -e PUSHGATEWAY_URL=<IP>:<порт> --restart always weather-bot:v0.0.1
```
Теперь бот готов к работе! Он сможет отвечать на команду `/weather`, показывая текущую температуру, давление и влажность в вашей комнате.

## Команды бота

-	`/start` — Приветственное сообщение и информация о том, что бот может сделать.
-	`/weather` — Получить текущую температуру, давление и влажность.

## Полезные советы

- Убедитесь, что у вас установлен Docker и все зависимости для Python из `requirements.txt`.
- Если хотите улучшить функционал, загляните в код бота и настройте его уже под свои нужды!

Теперь вы можете отслеживать погоду с помощью вашего Telegram бота “Cloudy with a Chance”!
<img width="457" alt="image" src="https://github.com/user-attachments/assets/5424ca50-a3e7-40e2-87b7-c5649846f1d5">

Еще строить свои дашборды в Grafana и создавать алерты:
![image](https://github.com/user-attachments/assets/b0544656-7bff-46ef-9566-0ace65647c95)
