#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import smtplib
import ssl
import html

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

        bcc.append("olaf.cazarez@cafe88.com")
        bcc.append("juancarlos.valenzuela@cafe88.com")

        content = content

        content = content.replace("#domain#", data["domain"])

        content = content.replace("#user_name#", data["name"])

        content = content.replace("#user_id#", data["user_id"])

        content = content.replace("#secure_id#", data["secure_id"])

        """ Create a text/plain message """
        msg = MIMEMultipart()
        msg["Subject"] = Header("Cafe88 - Bienvenido".encode("utf-8"), "utf-8")

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

        bcc.append("olaf.cazarez@cafe88.com")
        bcc.append("juancarlos.valenzuela@cafe88.com")

        content = content

        content = content.replace("#domain#", data["domain"])

        content = content.replace("#user_name#", data["name"])

        content = content.replace("#user_id#", data["user_id"])

        content = content.replace("#secure_id#", data["secure_id"])

        """ Create a text/plain message """
        msg = MIMEMultipart()
        msg["Subject"] = Header("Cafe88 - Recupera tu contraseña ".encode("utf-8"), "utf-8")

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

        to = data.get("to", [document["client"]["email"]])
        cc = []
        to = [
            "olaf.cazarez@cafe88.com",
            "juancarlos.valenzuela@cafe88.com",
            # document["client"]["email"]
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
        subject = "Cafe88 - Factura {} ".format(document["code"])

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

    def send_sale_note(self, data: dict = None):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)), template="send_sale.tpl.html"
        )

        document = data["document"]

        to = data.get("to", [document["client"]["email"]])
        cc = []
        bcc = [
            "olaf.cazarez@cafe88.com",
            "juancarlos.valenzuela@cafe88.com",
        ]

        if "cc" in data:
            cc = data["cc"]

        if "bcc" in data:
            bcc = data["bcc"]

        f = open(file_path, "r")
        content = f.read()

        content = content.replace("#client_name#", document["client"]["legal_name"])

        content = content.replace("#total#", "{:.2f}".format(document["total"]))

        """ Create a text/plain message """
        subject = "{} - Nota de venta {} ".format(
            document["company"]["trade_name"],
            document["code"],
        )

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

    def _send_html_message(
        self,
        subject,
        content,
        to,
        cc=None,
        bcc=None,
    ):
        to = to or []
        cc = cc or []
        bcc = bcc or []

        msg = MIMEMultipart()
        msg["Subject"] = Header(
            subject.encode("utf-8"),
            "utf-8",
        )

        msg["From"] = self.__settings["user"]
        msg["To"] = ",".join(to)
        msg["Cc"] = ",".join(cc)
        msg["Bcc"] = ",".join(bcc)

        body = MIMEText(
            content.encode("utf-8"),
            "html",
            _charset="utf-8",
        )

        msg.attach(body)

        ssl.create_default_context()

        server = smtplib.SMTP_SSL(
            self.__settings["server"],
            self.__settings["port"],
        )

        try:
            server.login(
                self.__settings["user"],
                self.__settings["password"],
            )

            server.sendmail(
                self.__settings["user"],
                to + cc + bcc,
                msg.as_string(),
            )
        finally:
            server.close()

        return True

    def _build_order_products_html(self, products):
        rows = []

        for item in products:
            name = html.escape(str(item.get("name", "Producto")))

            measure = html.escape(str(item.get("measure", "")))

            quantity = float(item.get("quantity", 0))

            price = float(item.get("price", 0))

            total = float(item.get("total", 0))

            rows.append(
                """
                <tr>
                    <td style="
                        padding: 12px 8px;
                        border-bottom: 1px solid #eadfd3;
                    ">
                        <strong>{name}</strong>
                        <div style="
                            margin-top: 4px;
                            color: #76665d;
                            font-size: 13px;
                        ">
                            {measure}
                        </div>
                    </td>

                    <td style="
                        padding: 12px 8px;
                        border-bottom: 1px solid #eadfd3;
                        text-align: center;
                        white-space: nowrap;
                    ">
                        {quantity:g}
                    </td>

                    <td style="
                        padding: 12px 8px;
                        border-bottom: 1px solid #eadfd3;
                        text-align: right;
                        white-space: nowrap;
                    ">
                        ${price:,.2f}
                    </td>

                    <td style="
                        padding: 12px 8px;
                        border-bottom: 1px solid #eadfd3;
                        text-align: right;
                        white-space: nowrap;
                    ">
                        <strong>${total:,.2f}</strong>
                    </td>
                </tr>
                """.format(
                    name=name,
                    measure=measure,
                    quantity=quantity,
                    price=price,
                    total=total,
                )
            )

        return "".join(rows)

    def _build_delivery_address_html(self, address):
        external_number = html.escape(
            str(
                address.get(
                    "address_external_number",
                    "",
                )
            )
        )

        internal_number = html.escape(
            str(
                address.get(
                    "address_internal_number",
                    "",
                )
            )
        )

        internal_text = ""

        if internal_number:
            internal_text = " Int. {}".format(internal_number)

        return """
            <strong>{name}</strong><br>
            {street} {external}{internal}<br>
            {neighborhood}<br>
            C.P. {zip}<br>
            {municipality}, {state}<br>
            Tel. {phone}<br>
            {email}
        """.format(
            name=html.escape(str(address.get("name", ""))),
            street=html.escape(
                str(
                    address.get(
                        "address_street",
                        "",
                    )
                )
            ),
            external=external_number,
            internal=internal_text,
            neighborhood=html.escape(
                str(
                    address.get(
                        "neighborhood",
                        "",
                    )
                )
            ),
            zip=html.escape(str(address.get("zip", ""))),
            municipality=html.escape(
                str(
                    address.get(
                        "municipality_name",
                        "",
                    )
                )
            ),
            state=html.escape(
                str(
                    address.get(
                        "state_name",
                        "",
                    )
                )
            ),
            phone=html.escape(str(address.get("phone", ""))),
            email=html.escape(str(address.get("email", ""))),
        )

    def send_order_confirmation(self, data):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)),
            template="order_confirmation.tpl.html",
        )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        document = data["document"]
        address = data["delivery_address"]
        payment = data["payment"]
        products = data.get("products", [])

        to = data.get(
            "to",
            [address["email"]],
        )

        cc = data.get("cc", [])
        bcc = data.get("bcc", [])

        replacements = {
            "#client_name#": html.escape(str(address.get("name", ""))),
            "#document_code#": html.escape(str(document.get("code", ""))),
            "#transaction_date#": html.escape(
                str(
                    document.get(
                        "transaction_date",
                        "",
                    )
                )
            ),
            "#products#": self._build_order_products_html(products),
            "#subtotal#": "{:,.2f}".format(float(document.get("subtotal", 0))),
            "#taxes#": "{:,.2f}".format(float(document.get("taxes", 0))),
            "#total#": "{:,.2f}".format(float(document.get("total", 0))),
            "#currency#": html.escape(
                str(
                    document.get(
                        "currency",
                        "MXN",
                    )
                ).upper()
            ),
            "#delivery_address#": self._build_delivery_address_html(address),
            "#payment_method#": "PayPal",
            "#payment_reference#": html.escape(
                str(
                    payment.get(
                        "provider_transaction_id",
                        "",
                    )
                )
            ),
        }

        for key, value in replacements.items():
            content = content.replace(
                key,
                value,
            )

        subject = ("Cafe88 - Hemos recibido tu pedido {}").format(document["code"])

        return self._send_html_message(
            subject=subject,
            content=content,
            to=to,
            cc=cc,
            bcc=bcc,
        )

    def send_order_notification(self, data):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)),
            template="order_notification.tpl.html",
        )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        document = data["document"]
        address = data["delivery_address"]
        payment = data["payment"]
        products = data.get("products", [])

        to = data.get("to", [])
        cc = data.get("cc", [])
        bcc = data.get("bcc", [])

        if not to:
            raise ValueError("Production recipients are required")

        replacements = {
            "#document_code#": html.escape(str(document.get("code", ""))),
            "#transaction_date#": html.escape(
                str(
                    document.get(
                        "transaction_date",
                        "",
                    )
                )
            ),
            "#client_name#": html.escape(str(address.get("name", ""))),
            "#client_phone#": html.escape(str(address.get("phone", ""))),
            "#client_email#": html.escape(str(address.get("email", ""))),
            "#products#": self._build_order_products_html(products),
            "#delivery_address#": self._build_delivery_address_html(address),
            "#references#": html.escape(
                str(
                    address.get(
                        "references",
                        "",
                    )
                )
            ),
            "#total#": "{:,.2f}".format(float(document.get("total", 0))),
            "#currency#": html.escape(
                str(
                    document.get(
                        "currency",
                        "MXN",
                    )
                ).upper()
            ),
            "#payment_reference#": html.escape(
                str(
                    payment.get(
                        "provider_transaction_id",
                        "",
                    )
                )
            ),
        }

        for key, value in replacements.items():
            content = content.replace(
                key,
                value,
            )

        subject = "Cafe88 - Nuevo pedido {}".format(document["code"])

        return self._send_html_message(
            subject=subject,
            content=content,
            to=to,
            cc=cc,
            bcc=bcc,
        )
