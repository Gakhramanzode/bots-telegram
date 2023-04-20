# Generate Bot

Generate Bot - это бот генерирует случайный никнейм, сложный пароль из 18 символов, номер логического порта для TCP/UDP. [Ссылка](https://t.me/generate_asker_bot) на пример бота.

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

После запуска бота вы можете использовать его для генерации никнеймов, паролей и логических портов. Для этого отправьте ему сообщение `/generate_nickname`, `/generate_password` или `/generate_port_number`. 

Пример диалога с ботом:
<img width="384" alt="Снимок экрана 2023-04-19 103909" src="https://user-images.githubusercontent.com/62985982/233398424-1aaa700a-ab13-474d-b3e1-c411b73c38a4.png">
