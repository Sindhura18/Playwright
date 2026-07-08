import os
import smtplib
from email.mime.text import MIMEText


def send_test_email(inbox_name, subject, body):
    """Sends a plain-text email from SMTP_USER (Gmail) to `inbox_name`@MAIL_DOMAIN
    using credentials from the environment. Returns the full recipient address used."""
    smtp_user = os.environ["SMTP_USER"]
    smtp_password = os.environ["SMTP_APP_PASSWORD"]
    mail_domain = os.getenv("MAIL_DOMAIN", "mailinator.com")
    to_address = f"{inbox_name}@{mail_domain}"

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = smtp_user
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [to_address], message.as_string())

    return to_address
