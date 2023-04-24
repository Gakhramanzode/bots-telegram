# Fußball Bot

Fußball Bot - это бот для Telegram, который помогает вам отслеживать расписание футбольных матчей.

## API

Для получения информации о футбольных матчах бот использует [API сервиса football-data.org](https://www.football-data.org/). Чтобы использовать бота, вам необходимо зарегистрироваться на [сайте](https://www.football-data.org/) и получить API-ключ.

## Команды

В настоящее время бот поддерживает следующие футбольные команды:

- Napoli
- Liverpool
- Chelsea
- Manchester City
- Marseille
- Bayern München

Вы можете добавить новые команды, отредактировав код бота.

## Установка

Для запуска Fußball Bot на CentOS 7 вам потребуются следующие библиотеки:

- Python 3
- python-telegram-bot
- requests
- pytz
- schedule

Вы можете установить их с помощью следующих команд:

```
sudo yum install python3 -y
sudo pip3 install python-telegram-bot requests pytz schedule
```

## Запуск

Чтобы запустить Fußball Bot, перейдите в папку с кодом и выполните следующую команду:

`python3 bot-fußball.py`

## Использование

После запуска бота вы можете использовать его для отслеживания расписания футбольных матчей.