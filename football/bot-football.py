import requests
from datetime import datetime, time, timedelta
import pytz
import schedule
import time as t
import os
from ics import Calendar, Event

TOKEN = os.environ.get('football_TOKEN')
CHAT_ID = os.environ.get('football_CHAT_ID')
API_TOKEN = os.environ.get('football_API_TOKEN')

TEAMS = {
    113: "Napoli",
    64: "Liverpool",
    61: "Chelsea",
    65: "Manchester City",
    516: "Marseille",
    5: "Bayern München",
    4: "Borussia Dortmund",
    100: "AS Roma",
    3: "Bayer 04 Leverkusen"
}

def get_upcoming_matches(team_id):
    url = f"http://api.football-data.org/v2/teams/{team_id}/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(url, headers=headers)
    data = response.json()
    matches = []
    now = datetime.utcnow()
    week_from_now = now + timedelta(days=7)
    moscow_tz = pytz.timezone("Europe/Moscow")
    # print(data)
    for match in data["matches"]:
        utc_date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
        if utc_date > now and utc_date < week_from_now:
            print(data)
            moscow_date = utc_date.replace(tzinfo=pytz.utc).astimezone(moscow_tz)
            date = moscow_date.strftime("%d %B %Y %H:%M")
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            matches.append(f"*{home_team}* vs *{away_team}* on *{date}* (Moscow time)")
    return matches

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def create_ics_file(match, date):
    cal = Calendar()
    event = Event()
    event.name = match
    event.begin = date
    cal.events.add(event)
    file_path = f"{match}.ics"
    with open(file_path, 'w') as f:
        f.writelines(cal)
    return file_path

def send_ics_file(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    files = {'document': open(file_path, 'rb')}
    data = {"chat_id": CHAT_ID}
    requests.post(url, files=files, data=data)

def job():
    message = ""
    for team_id, team_name in TEAMS.items():
        matches = get_upcoming_matches(team_id)
        if matches:
            message += f"Upcoming *{team_name}* matches within the next week:\n" + "\n".join([f"**{match}**" for match in matches]) + "\n\n"
            for match in matches:
                match_date_str = match.split(" on ")[-1].replace("*", "")
                match_date = datetime.strptime(match_date_str, "%d %B %Y %H:%M (Moscow time)").strftime("%Y-%m-%d %H:%M:%S")
                file_path = create_ics_file(match, match_date)
                send_ics_file(file_path)
        else:
            message += f"No upcoming **{team_name}** matches within the next week found.\n\n"
    send_message(message)


moscow_tz = pytz.timezone("Europe/Moscow")
moscow_time = datetime.now(moscow_tz)
moscow_time_20_30 = moscow_tz.localize(datetime.combine(moscow_time.date(), time(13, 13)), is_dst=None)
utc_time_20_30 = moscow_time_20_30.astimezone(pytz.utc).strftime('%H:%M')

schedule.every().friday.at(utc_time_20_30).do(job)

if os.environ.get('CI'):
    exit(0)

while True:
    schedule.run_pending()
    t.sleep(1)