[![Run tests and deploy "bot-weather"](https://github.com/Gakhramanzode/bots-telegram/actions/workflows/bot-weather.yml/badge.svg)](https://github.com/Gakhramanzode/bots-telegram/actions/workflows/bot-weather.yml)
# :sun_behind_rain_cloud: Weather Bot

Weather Bot - это телеграм-бот, который помогает вам узнавать прогноз погоды.

## API

Для получения информации о погоде бот использует API сервиса OpenWeatherMap. Чтобы использовать бота, вам необходимо зарегистрироваться на сайте OpenWeatherMap и получить API-ключ.

## Установка

Для запуска Weather Bot на CentOS 7 вам потребуются:

- Python 3
- python-telegram-bot
- requests
- prometheus_client

Вы можете установить их с помощью следующих команд:

```bash
$ sudo yum install python3 -y
$ sudo pip3 install python-telegram-bot requests
```

Для запуска бота в docker-контейнере вам потребуется собрать docker-образ:
```bash
$ docker build -t bot-weather:v0.0.1 .
``` 

## Запуск

Чтобы нативно запустить Weather Bot, перейдите в папку с кодом и выполните следующую команду:

```bash
python3 bot-weather.py
```

Чтобы запустить в docker-контейнере, выполните команду:

```bash
$ docker run -d -p <ip-адрес>:57899:57899 \
--name bot-weather \
-e weather_TOKEN=токен_телеграм_бота \
-e weather_CHAT_ID=индентификатор_чата \
-e weather_API_KEY=api-ключ \
-e weather_CITY_ID=индентификатор_города \
-e weather_TIMEZONE=часовой_пояс \
-e weather_CITY_1_LAT=широта \
-e weather_CITY_1_LON=долгота \
-e weather_CITY_2_LAT=широта
-e weather_CITY_2_LON=долгота \
--restart always \
bot-weather:v0.0.1
```

## Использование

После запуска бота вы можете использовать его для получения прогноза погоды. 
