[![Run tests and deploy "bot-generate"](https://github.com/Gakhramanzode/bots-telegram/actions/workflows/bot-generate.yml/badge.svg)](https://github.com/Gakhramanzode/bots-telegram/actions/workflows/bot-generate.yml)
# :twisted_rightwards_arrows: Generate Bot

Generate Bot - это бот генерирует случайный никнейм, сложный пароль из 18 символов, номер логического порта для TCP/UDP. [Ссылка](https://t.me/generate_asker_bot) на пример бота.

## Установка

Для запуска Generate Bot на CentOS 7 вам потребуются следующие библиотеки:

- Python 3.9
- python-telegram-bot
- bot-football

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

После запуска бота вы можете использовать его для генерации никнеймов, паролей, логических портов. Для этого отправьте ему сообщение `/generate_nickname`, `/generate_password` или `/generate_port_number`. 

Пример диалога с ботом:

<img width="385" alt="Снимок экрана 2023-04-20 173537" src="https://user-images.githubusercontent.com/62985982/233399773-1260186a-201a-4ff0-9da8-755d6f120a28.png">
