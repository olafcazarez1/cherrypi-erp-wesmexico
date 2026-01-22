#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
import ssl

from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from utils.singleton_meta import MetaConfig


class Notification(object):

    def __init__(self, conn="smtp"):
        meta = MetaConfig.instance()
        self.__settings = meta.get_config(conn)

    def send_welcome_message(self, data):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)), template="welcome_message.tpl.html"
        )

        f = open(file_path, "r")
        content = f.read()

        to = []
        cc = []
        bcc = []

        to.append(data["email"])

        bcc.append("olaf.cazarez@wesmexico.com")
        bcc.append("juancarlos.valenzuela@wesmexico.com")

        content = content

        content = content.replace("#domain#", data["domain"])

        content = content.replace("#user_name#", data["name"])

        content = content.replace("#user_id#", data["user_id"])

        content = content.replace("#secure_id#", data["secure_id"])

        """ Create a text/plain message """
        msg = MIMEMultipart()
        msg["Subject"] = Header("WesMexico - Bienvenido".encode("utf-8"), "utf-8")

        msg["From"] = self.__settings["user"]

        msg["To"] = ",".join(to)
        msg["Cc"] = ",".join(cc)
        msg["Bcc"] = ",".join(bcc)

        """ The main body is just another attachment """
        body = MIMEText(content.encode("utf-8"), "html", _charset="utf-8")
        msg.attach(body)

        # Create a secure SSL context
        ssl.create_default_context()

        s = smtplib.SMTP_SSL(self.__settings["server"], self.__settings["port"])

        s.login(self.__settings["user"], self.__settings["password"])

        s.sendmail(self.__settings["user"], to + cc + bcc, msg.as_string())

        s.close()

        return True

    def send_restore_password(self, data):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)), template="restore_password.tpl.html"
        )

        f = open(file_path, "r")
        content = f.read()

        to = []
        cc = []
        bcc = []

        to.append(data["email"])

        bcc.append("olaf.cazarez@wesmexico.com")
        bcc.append("juancarlos.valenzuela@wesmexico.com")

        content = content

        content = content.replace("#domain#", data["domain"])

        content = content.replace("#user_name#", data["name"])

        content = content.replace("#user_id#", data["user_id"])

        content = content.replace("#secure_id#", data["secure_id"])

        """ Create a text/plain message """
        msg = MIMEMultipart()
        msg["Subject"] = Header("WesMexico - Recupera tu contraseña ".encode("utf-8"), "utf-8")

        msg["From"] = self.__settings["user"]

        msg["To"] = ",".join(to)
        msg["Cc"] = ",".join(cc)
        msg["Bcc"] = ",".join(bcc)

        """ The main body is just another attachment """
        body = MIMEText(content.encode("utf-8"), "html", _charset="utf-8")
        msg.attach(body)

        # Create a secure SSL context
        ssl.create_default_context()

        s = smtplib.SMTP_SSL(self.__settings["server"], self.__settings["port"])

        s.login(self.__settings["user"], self.__settings["password"])

        s.sendmail(self.__settings["user"], to + cc + bcc, msg.as_string())

        s.close()

        return True

    def send_signed_invoice(self, data: dict = None):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)), template="send_invoice.tpl.html"
        )

        document = data["document"]

        to = [
            # 'olaf.cazarez@wesmexico.com'
            document["client"]["email"]
        ]
        cc = []
        bcc = []

        if "cc" in data:
            cc = data["cc"]

        if "bcc" in data:
            bcc = data["bcc"]

        f = open(file_path, "r")
        content = f.read()

        content = content.replace("#client_name#", document["client"]["legal_name"])

        content = content.replace("#total#", "{:.2f}".format(document["total"]))

        """ Create a text/plain message """
        subject = "WesMexico - Factura {} ".format(document["code"])

        msg = MIMEMultipart()
        msg["Subject"] = Header(subject.encode("utf-8"), "utf-8")

        msg["From"] = self.__settings["user"]

        msg["To"] = ",".join(to)
        msg["Cc"] = ",".join(cc)

        """ The main body is just another attachment """
        body = MIMEText(content.encode("utf-8"), "html", _charset="utf-8")

        attachment = MIMEApplication(data["report"].read(), _subtype="zip")
        attachment.add_header("Content-Disposition", "attachment", filename=str(data["report_name"]))

        msg.attach(body)
        msg.attach(attachment)

        # Create a secure SSL context
        ssl.create_default_context()

        # print(self.__settings)
        s = smtplib.SMTP_SSL(self.__settings["server"], self.__settings["port"])

        s.login(self.__settings["user"], self.__settings["password"])

        s.sendmail(self.__settings["user"], to + cc + bcc, msg.as_string())

        s.close()

        return True
