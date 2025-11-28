import smtplib
from email.mime.text import MIMEText

GMAIL_USER = "chupakchowdary@gmail.com"
GMAIL_APP_PASSWORD = "qgzy nqxw qzlf yoja"

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)

    print("📩 Email sent!")
