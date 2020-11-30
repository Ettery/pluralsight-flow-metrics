from os.path import basename
from typing import List

# SMTP imports
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

# Outlook
import win32com.client as win32

def send_outlook_mail(send_from: str, send_to: str, subject: str, body: str, files:List[str]=None, suppress=True):

    if suppress and (send_to != send_from):
        return

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = send_to
    mail.Subject = subject
    mail.Body = body

    for attachment in files or []:
        mail.Attachments.Add(attachment)

    mail.Send()

    
# Not in use because our SMTP server has been locked down
def send_smtp_mail(send_from, send_to, subject, text, files=None, server="devsmtp1-agct", suppress=True):

    if suppress and (send_to != send_from):
        return

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
