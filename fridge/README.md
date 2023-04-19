# Fridge Bot

Fridge Bot - это бот для Telegram, который помогает вам отслеживать содержимое вашего холодильника.

## Установка

Для запуска Fridge Bot на CentOS 7 вам потребуются следующие библиотеки:

- Python 3.9
- python-telegram-bot

Вы можете установить их с помощью следующих команд:

`sudo yum install python3 -y`

```
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel
cd /opt
sudo wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
sudo tar xzf Python-3.9.0.tgz
cd Python-3.9.0
sudo ./configure --enable-optimizations
sudo make altinstall
```

`pip3.9 install pyTelegramBotAPI mysql-connector-python`

## Запуск

Чтобы запустить Fridge Bot, перейдите в папку с кодом и выполните следующую команду:

`python3.9 bot-fridge.py`

## Использование

После запуска бота вы можете использовать его для отслеживания содержимого вашего холодильника. Для этого отправьте ему сообщение `/start`.