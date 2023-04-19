# Weather Bot

Weather Bot - это бот для Telegram, который помогает вам узнавать прогноз погоды.

## API

Для получения информации о погоде бот использует API сервиса OpenWeatherMap. Чтобы использовать бота, вам необходимо зарегистрироваться на сайте OpenWeatherMap и получить API-ключ.

## Установка

Для запуска Weather Bot на CentOS 7 вам потребуются следующие библиотеки:

- Python 3
- python-telegram-bot
- requests

Вы можете установить их с помощью следующих команд:

```
sudo yum install python3 -y
sudo pip3 install python-telegram-bot requests
```

## Запуск

Чтобы запустить Weather Bot, перейдите в папку с кодом и выполните следующую команду:

`python3 bot-weather.py`

## Использование

После запуска бота вы можете использовать его для получения прогноза погоды. 