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

        to = data.get("to")
        cc = []
        bcc = []

        if "cc" in data:
            cc = data["cc"]

        if "bcc" in data:
            bcc = data["bcc"]

        f = open(file_path, "r")
        content = f.read()

        content = content.replace("#company_name#", document["company"]["legal_name"])
        content = content.replace("#client_name#", document["client"]["legal_name"])

        content = content.replace("#total#", "{:.2f}".format(document["total"]))
        content = content.replace("#invoice_code#", document["code"])

        taxpayer_id = (document["company"].get("taxpayer_id") or "").strip().upper()

        taxpayer_id = (document.get("company", {}).get("taxpayer_id") or "").strip().upper()

        bank_accounts = {
            "GJM0804022S3": {
                "bank": "BBVA",
                "beneficiary": "Grupo JUCAVZA de México",
                "account": "0161201921",
                "clabe": "012730001612019212",
                "rfc": "GJM0804022S3",
            },
            "VAAJ780903F8A": {
                "bank": "Azteca",
                "beneficiary": "Juan Carlos Valenzuela Angulo",
                "account": "2098 1377 8837 42",
                "clabe": "1277 3001 3778 8374 28",
                "rfc": "VAAJ780903F8A",
            },
        }

        bank_information = ""
        bank = bank_accounts.get(taxpayer_id)

        if bank:
            bank_information = """
            <table role="presentation" width="100%" cellpadding="0"
                cellspacing="0" border="0"
                style="margin-top:26px; border:1px solid #e5e9ef;
                        border-collapse:collapse;">

                <tr>
                    <td colspan="2"
                        style="padding:16px 20px; background-color:#f5f8fc;
                            font-size:15px; font-weight:bold; color:#173b63;">
                        Datos bancarios para transferencia
                    </td>
                </tr>

                <tr>
                    <td style="padding:16px 20px 6px; font-size:12px;
                            color:#65758a;">
                        BANCO
                    </td>
                    <td style="padding:16px 20px 6px; font-size:12px;
                            color:#65758a;">
                        BENEFICIARIO
                    </td>
                </tr>

                <tr>
                    <td style="padding:0 20px 16px; font-size:15px;
                            font-weight:bold; color:#273244;">
                        {bank}
                    </td>
                    <td style="padding:0 20px 16px; font-size:14px;
                            font-weight:bold; color:#273244;">
                        {beneficiary}
                    </td>
                </tr>

                <tr>
                    <td colspan="2"
                        style="padding:14px 20px; border-top:1px solid #e9edf2;">
                        <div style="font-size:12px; color:#65758a;">
                            NÚMERO DE CUENTA
                        </div>
                        <div style="font-size:16px; font-weight:bold;
                                    color:#273244; margin-top:5px;">
                            {account}
                        </div>
                    </td>
                </tr>

                <tr>
                    <td colspan="2"
                        style="padding:14px 20px; border-top:1px solid #e9edf2;">
                        <div style="font-size:12px; color:#65758a;">
                            CLABE INTERBANCARIA
                        </div>
                        <div style="font-size:16px; font-weight:bold;
                                    color:#173b63; margin-top:5px;">
                            {clabe}
                        </div>
                    </td>
                </tr>

                <tr>
                    <td colspan="2"
                        style="padding:14px 20px; border-top:1px solid #e9edf2;">
                        <div style="font-size:12px; color:#65758a;">
                            RFC
                        </div>
                        <div style="font-size:14px; font-weight:bold;
                                    color:#273244; margin-top:5px;">
                            {rfc}
                        </div>
                    </td>
                </tr>

                <tr>
                    <td colspan="2"
                        style="padding:14px 20px; background-color:#fafbfd;
                            border-top:1px solid #e9edf2;
                            font-size:12px; line-height:1.7; color:#65758a;">
                        Favor de indicar el número de factura como referencia
                        al realizar la transferencia.
                    </td>
                </tr>

            </table>
            """.format(**bank)

        content = content.replace("#bank_information#", bank_information)

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

    def send_sale_note(self, data: dict = None):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)), template="send_sale.tpl.html"
        )

        document = data["document"]

        to = data.get("to", [document["client"]["email"]])
        cc = []
        bcc = [
            "olaf.cazarez@wesmexico.com",
            "juancarlos.valenzuela@wesmexico.com",
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
            "#payment_method#": payment.get("provider").replace("_", " ").title(),
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

        subject = ("WesMexico - Hemos recibido tu pedido {}").format(document["code"])

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
            "#payment_method#": payment.get("provider", "").replace("_", " ").title(),
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

        subject = "WesMexico - Nuevo pedido {}".format(document["code"])

        return self._send_html_message(
            subject=subject,
            content=content,
            to=to,
            cc=cc,
            bcc=bcc,
        )

    def send_lodging_reservation_confirmation(
        self,
        data,
    ):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)),
            template="lodging_reservation_confirmation.tpl.html",
        )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        reservation = data["reservation"]
        lodging = data["lodging"]
        payment = data["payment"]

        total = float(
            data.get(
                "total",
                0,
            )
            or 0
        )

        guest_name = "{} {}".format(
            reservation.get(
                "first_name",
                "",
            ),
            reservation.get(
                "last_name",
                "",
            ),
        ).strip()

        to = data.get(
            "to",
            [
                reservation["email"],
            ],
        )

        cc = data.get(
            "cc",
            [],
        )

        bcc = data.get(
            "bcc",
            [],
        )

        payment_reference = payment.get(
            "provider_payment_id",
            "",
        ) or payment.get(
            "provider_reference",
            "",
        )

        replacements = {
            "#guest_name#": html.escape(guest_name),
            "#reservation_code#": html.escape(
                str(
                    reservation.get(
                        "code",
                        "",
                    )
                )
            ),
            "#lodging_name#": html.escape(
                str(
                    lodging.get(
                        "name",
                        "",
                    )
                )
            ),
            "#check_in#": html.escape(
                str(
                    reservation.get(
                        "check_in",
                        "",
                    )
                )
            ),
            "#check_out#": html.escape(
                str(
                    reservation.get(
                        "check_out",
                        "",
                    )
                )
            ),
            "#nights#": html.escape(
                str(
                    reservation.get(
                        "nights",
                        "",
                    )
                )
            ),
            "#guests#": html.escape(
                str(
                    reservation.get(
                        "guests",
                        "",
                    )
                )
            ),
            "#total#": "{:,.2f}".format(total),
            "#currency#": html.escape(
                str(
                    reservation.get(
                        "currency",
                        "MXN",
                    )
                ).upper()
            ),
            "#payment_method#": html.escape(
                str(
                    payment.get(
                        "provider",
                        "",
                    )
                )
                .replace(
                    "_",
                    " ",
                )
                .title()
            ),
            "#payment_reference#": html.escape(str(payment_reference)),
            "#guest_email#": html.escape(
                str(
                    reservation.get(
                        "email",
                        "",
                    )
                )
            ),
            "#guest_phone#": html.escape(
                str(
                    reservation.get(
                        "phone",
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

        subject = ("Por La Baja - Reservación confirmada {}").format(
            reservation.get(
                "code",
                "",
            )
        )

        return self._send_html_message(
            subject=subject,
            content=content,
            to=to,
            cc=cc,
            bcc=bcc,
        )

    def send_lodging_reservation_notification(
        self,
        data,
    ):
        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)),
            template="lodging_reservation_notification.tpl.html",
        )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

        reservation = data["reservation"]
        lodging = data["lodging"]
        payment = data["payment"]
        charges = data.get(
            "charges",
            [],
        )

        total = float(
            data.get(
                "total",
                0,
            )
            or 0
        )

        to = data.get(
            "to",
            [],
        )

        cc = data.get(
            "cc",
            [],
        )

        bcc = data.get(
            "bcc",
            [],
        )

        if not to:

            raise ValueError("Reservation notification recipients are required")

        guest_name = "{} {}".format(
            reservation.get(
                "first_name",
                "",
            ),
            reservation.get(
                "last_name",
                "",
            ),
        ).strip()

        payment_reference = payment.get(
            "provider_payment_id",
            "",
        ) or payment.get(
            "provider_reference",
            "",
        )

        replacements = {
            "#reservation_code#": html.escape(
                str(
                    reservation.get(
                        "code",
                        "",
                    )
                )
            ),
            "#lodging_name#": html.escape(
                str(
                    lodging.get(
                        "name",
                        "",
                    )
                )
            ),
            "#lodging_code#": html.escape(
                str(
                    lodging.get(
                        "code",
                        "",
                    )
                )
            ),
            "#guest_name#": html.escape(guest_name),
            "#guest_email#": html.escape(
                str(
                    reservation.get(
                        "email",
                        "",
                    )
                )
            ),
            "#guest_phone#": html.escape(
                str(
                    reservation.get(
                        "phone",
                        "",
                    )
                )
            ),
            "#check_in#": html.escape(
                str(
                    reservation.get(
                        "check_in",
                        "",
                    )
                )
            ),
            "#check_out#": html.escape(
                str(
                    reservation.get(
                        "check_out",
                        "",
                    )
                )
            ),
            "#nights#": html.escape(
                str(
                    reservation.get(
                        "nights",
                        "",
                    )
                )
            ),
            "#guests#": html.escape(
                str(
                    reservation.get(
                        "guests",
                        "",
                    )
                )
            ),
            "#adults#": html.escape(
                str(
                    reservation.get(
                        "adults",
                        "",
                    )
                )
            ),
            "#children#": html.escape(
                str(
                    reservation.get(
                        "children",
                        "",
                    )
                )
            ),
            "#total#": "{:,.2f}".format(total),
            "#currency#": html.escape(
                str(
                    reservation.get(
                        "currency",
                        "MXN",
                    )
                ).upper()
            ),
            "#payment_method#": html.escape(
                str(
                    payment.get(
                        "provider",
                        "",
                    )
                )
                .replace(
                    "_",
                    " ",
                )
                .title()
            ),
            "#payment_reference#": html.escape(str(payment_reference)),
            "#observations#": html.escape(
                str(
                    reservation.get(
                        "observations",
                        "",
                    )
                    or ""
                )
            ),
        }

        for key, value in replacements.items():

            content = content.replace(
                key,
                value,
            )

        subject = ("Por La Baja - Nueva reservación {}").format(
            reservation.get(
                "code",
                "",
            )
        )

        return self._send_html_message(
            subject=subject,
            content=content,
            to=to,
            cc=cc,
            bcc=bcc,
        )

    def send_lodging_transfer_review_notification(self, data):

        file_path = "{base}/notification_templates/{template}".format(
            base=os.path.dirname(os.path.abspath(__file__)),
            template="lodging_transfer_review.tpl.html",
        )

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        reservation = data["reservation"]
        lodging = data["lodging"]
        payment = data["payment"]
        review = data["review"]

        guest_name = "{} {}".format(
            reservation.get("first_name", ""),
            reservation.get("last_name", ""),
        ).strip()

        replacements = {
            "#reservation_code#": reservation.get("code", ""),
            "#guest_name#": guest_name,
            "#guest_email#": reservation.get("email", ""),
            "#guest_phone#": reservation.get("phone", ""),
            "#lodging_name#": lodging.get("name", ""),
            "#check_in#": reservation.get("check_in", ""),
            "#check_out#": reservation.get("check_out", ""),
            "#amount#": "{:,.2f}".format(float(payment.get("amount") or 0)),
            "#currency#": str(payment.get("currency", "MXN")).upper(),
            "#receipt_url#": data["receipt_url"],
            "#review_url#": data["review_url"],
        }

        for key, value in replacements.items():
            content = content.replace(
                key,
                html.escape(str(value), quote=True),
            )

        subject = "Por La Baja - Transferencia por verificar {}".format(reservation.get("code", ""))

        return self._send_html_message(
            subject=subject,
            content=content,
            to=data["to"],
            cc=data.get("cc", []),
            bcc=data.get("bcc", []),
        )
