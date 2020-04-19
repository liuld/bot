#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_


from email.mime.text import MIMEText
import smtplib
import logging


def send_mail(to_mail, to_title, to_content, password):

    from_mail = "linchqd@163.com"
    mail_server = 'smtp.163.com'
    mail_port = 465
    mail_user = from_mail
    mail_pass = password

    message = MIMEText(to_content, 'plain', 'utf-8')
    message['From'] = "{}".format(from_mail)
    message['To'] = ",".join(to_mail) if to_mail is list else to_mail
    message['Subject'] = to_title

    try:
        client = smtplib.SMTP_SSL(mail_server, mail_port)
        client.ehlo()
        client.login(mail_user, mail_pass)
        client.sendmail(from_mail, to_mail, message.as_string())
        client.quit()
    except smtplib.SMTPException as e:
        logging.error('{}'.format(e))
