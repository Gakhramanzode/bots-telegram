import requests
from datetime import datetime, time, timedelta
import pytz
import schedule
import time as t
import os
from ics import Calendar, Event
import logging

# ==========================
# Настройка логирования
# ==========================
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Скрываем детальные логи telegram / httpx, чтобы не утекал токен
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.vendor.ptb_urllib3.urllib3.connectionpool').setLevel(logging.WARNING)

# ==========================
# Переменные окружения
# ==========================
TOKEN = os.environ.get('football_TOKEN')
CHAT_ID = os.environ.get('football_CHAT_ID')
API_TOKEN = os.environ.get('football_API_TOKEN')

# Словарь с командами и их ID
TEAMS = {
    5: "Bayern München",
    3: "Bayer 04 Leverkusen",
    4: "Borussia Dortmund",
    113: "Napoli",
    100: "AS Roma",
    65: "Manchester City",
    61: "Chelsea",
    64: "Liverpool",
    516: "Marseille"
}

def get_upcoming_matches(team_id):
    """
    Получение предстоящих матчей для указанной команды.
    """
    url = f"http://api.football-data.org/v2/teams/{team_id}/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": API_TOKEN}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        matches = []
        now = datetime.utcnow()
        week_from_now = now + timedelta(days=7)
        moscow_tz = pytz.timezone("Europe/Moscow")
        
        for match in data.get("matches", []):
            utc_date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
            if now < utc_date < week_from_now:
                moscow_date = utc_date.replace(tzinfo=pytz.utc).astimezone(moscow_tz)
                date_str = moscow_date.strftime("%d %B %Y %H:%M")
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                match_info = f"*{home_team}* 🆚 *{away_team}* on *{date_str}* (Moscow time)"
                matches.append(match_info)
        logging.info(f"Найдено {len(matches)} матч(ей) для команды ID {team_id}.")
        return matches
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе матчей для команды ID {team_id}: {e}")
        return []
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        return []

def send_message(text):
    """
    Отправка текстового сообщения в Telegram.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info("Сообщение успешно отправлено в Telegram.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

def create_ics_file(matches):
    """
    Создание .ics файла с предстоящими матчами.
    """
    cal = Calendar()
    for match in matches:
        try:
            event = Event()
            event.name = match
            # Извлечение даты и времени из строки
            match_date_str = match.split(" on ")[-1].replace("*", "").split(" (")[0]
            event.begin = datetime.strptime(match_date_str, "%d %B %Y %H:%M")
            event.duration = timedelta(hours=2)  # Предполагаемая продолжительность матча
            cal.events.add(event)
        except Exception as e:
            logging.error(f"Ошибка при создании события для матча '{match}': {e}")
    current_date = datetime.now().strftime("%d-%m-%Y")
    file_path = f"matches_{current_date}.ics"
    try:
        with open(file_path, 'w') as f:
            f.writelines(cal)
        logging.info(f".ics файл создан: {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Ошибка при записи .ics файла: {e}")
        return None

def send_ics_file(file_path):
    """
    Отправка .ics файла в Telegram.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as document:
            files = {'document': document}
            data = {"chat_id": CHAT_ID}
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
        logging.info(f".ics файл успешно отправлен: {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке .ics файла: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка при отправке .ics файла: {e}")

def job():
    """
    Основная задача для планировщика: получение матчей и отправка сообщений.
    """
    logging.info("Запуск задачи по получению и отправке матчей.")
    message = ""
    all_matches = []
    for team_id, team_name in TEAMS.items():
        matches = get_upcoming_matches(team_id)
        if matches:
            message += f"Upcoming *{team_name}* matches within the next week:\n" + "\n".join([f"**{match}**" for match in matches]) + "\n\n"
            all_matches.extend(matches)
        else:
            message += f"No upcoming *{team_name}* matches within the next week found.\n\n"
    send_message(message)
    if all_matches:
        file_path = create_ics_file(all_matches)
        if file_path:
            send_ics_file(file_path)
            try:
                os.remove(file_path)
                logging.info(f".ics файл удалён: {file_path}")
            except Exception as e:
                logging.error(f"Ошибка при удалении .ics файла: {e}")

# Настройка времени запуска задачи
moscow_tz = pytz.timezone("Europe/Moscow")
moscow_time = datetime.now(moscow_tz)

# Устанавливаем время запуска на понедельник в 16:31 по Москве
scheduled_time = time(16, 31)
moscow_time_scheduled = moscow_tz.localize(datetime.combine(moscow_time.date(), scheduled_time), is_dst=None)
utc_time_scheduled = moscow_time_scheduled.astimezone(pytz.utc).strftime('%H:%M')

# Планируем задачу каждую понедельник в указанное время
schedule.every().monday.at(utc_time_scheduled).do(job)
logging.info(f"Задача запланирована на понедельник в {utc_time_scheduled} UTC.")

# Бесконечный цикл для запуска планировщика
logging.info("Бот запущен и ожидает выполнения задач.")
while True:
    schedule.run_pending()
    t.sleep(1)

