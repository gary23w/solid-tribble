import smtplib
import datetime


class SendMail:
    def __init__(self, name, _object):
        print(name, "mail object created", datetime.date.today())
        self._object = _object

    def mailer(self):
        email = "SMTP"
        password = "passwurd1"
        message_sub = datetime.date.today()
        message_bod = self._object
        message = "Subject: {}\n\n{}".format(message_sub, message_bod)
        server = smtplib.SMTP("smtp.HOST.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, "destination@dest.dest", message)
        print("Internal Mail System: data transfer complete:", datetime.date.today())


