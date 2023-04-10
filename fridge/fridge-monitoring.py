import os
import smtplib
from email.mime.text import MIMEText
import datetime

with open('/path/to/log/file.log', 'a') as f:
    f.write(f'Script started at {datetime.datetime.now()}\n')

def send_email(subject, body):
    sender = "your_email@example.com"
    password = "your_password"
    recipient = "recipient@example.com"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()

def check_service_status():
    output = os.popen('systemctl status fridge.service').read()
    if 'Active: active (running)' not in output:
        subject = "fridge.service is not running"
        body = f"fridge.service is not running. systemctl status output:\n\n{output}"
        send_email(subject, body)

check_service_status()
