import glob
import os
import imghdr
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

SENDER = "pythonbyfebash@gmail.com"
PASSWORD = os.getenv("PASSWORD")
reciever = "pythonbyfebash@gmail.com"
HOST= "smtp.gmail.com"
PORT = 587


def send_mail(filepath):
    email_message = EmailMessage()
    email_message["Subject"] = "Change detected!"
    email_message.set_content("Hey, new object detected!!")

    with open(filepath,'rb') as file:
        content = file.read()
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))


    server = smtplib.SMTP(HOST,PORT)
    server.ehlo()
    server.starttls()
    server.login(SENDER,PASSWORD)
    server.sendmail(SENDER,reciever,email_message.as_string())
    server.quit()


if __name__ == "__main__":
    send_mail("images/frame7.png")