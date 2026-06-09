#!/usr/bin/env python3
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT   = 587
FROM        = "julien.pajor@naxos.fr"
PASSWORD    = os.environ["EMAIL_PASSWORD"]
TO          = ["julien.pajor@naxos.fr"]
HTML_FILE   = "veille.html"

def send():
    today   = date.today().strftime("%d %B %Y")
    subject = f"Veille Immobilier & Proptech — {today}"

    msg = MIMEMultipart("mixed")
    msg["From"]    = FROM
    msg["To"]      = ", ".join(TO)
    msg["Subject"] = subject

    msg.attach(MIMEText(
        f"Bonjour,\n\nVeuillez trouver en pièce jointe la veille concurrentielle Immobilier & Proptech du {today}.\n\nBonne lecture,\nNaxos",
        "plain", "utf-8"
    ))

    with open(HTML_FILE, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="veille-immobilier-{today}.html"')
    msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(FROM, PASSWORD)
        server.sendmail(FROM, TO, msg.as_string())

    print(f"✅ Email envoyé à {', '.join(TO)}")

if __name__ == "__main__":
    send()
