# :twisted_rightwards_arrows: Generate Bot

Generate Bot - это телеграм-бот, который генерирует пин-код, никнейм, номер логического порта для TCP/UDP или пароль.

## Запуск
Для запуска бота в docker-контейнере вам потребуется собрать docker-образ:
```bash
docker build -t bot-generate:v0.1.0 .
```
Переходим в telegram, пишем https://t.me/BotFather, создаем своего бота и получаем от него токен.

Чтобы запустить в docker-контейнере, выполняем команду:
```bash
docker run --name bot-generate \
--restart always \
-e GENERATE_BOT_TOKEN="токен_телеграм_бота" \
bot-generate:v0.1.0
```
## Использование

После запуска бота вы можете использовать его для генерации никнеймов, паролей, логических портов. Для этого отправьте ему сообщение `/generate_nickname`, `/generate_password` или `/generate_port_number`. 

Пример диалога с ботом:
<img width="385" alt="Снимок экрана 2023-04-20 173537" src="https://user-images.githubusercontent.com/62985982/233399773-1260186a-201a-4ff0-9da8-755d6f120a28.png">
