import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .email_config import EMAIL, PASSWORD, SERVER, PORT

def send_email(subject, body, to_email):
    # Email configuration
    sender_email = EMAIL
    sender_password = PASSWORD
    smtp_server = SERVER
    smtp_port = PORT

    # Create a MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach body to the email
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS for security
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
