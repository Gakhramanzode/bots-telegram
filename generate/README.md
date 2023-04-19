# Generate Bot

Generate Bot - это бот генерирует случайный никнейм и сложный пароль из 18 символов. [Ссылка](https://t.me/generate_asker_bot) на пример бота.

## Установка

Для запуска Generate Bot на CentOS 7 вам потребуются следующие библиотеки:

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

## Запуск

Чтобы запустить Fridge Bot, перейдите в папку с кодом и выполните следующую команду:

`python3.9 bot-generate.py`

## Использование

После запуска бота вы можете использовать его для генерации никнеймов и паролей. Для этого отправьте ему сообщение `/generate_nickname` или `/generate_password`. 

Вот пример диалога с ботом:

