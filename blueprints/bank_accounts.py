import json
import uuid
import cherrypy
import pymysql
import logging

from datetime import datetime
from utils.decorators import tools
from utils.query import _OR, _AND, Query
from utils.utils import Utils

from helpers.helper_account_relation import HelperAccountRelation

from models.serie import Serie
from models.user import User
from models.user_employee import UserEmployee

from models.company_bank_account import CompanyBankAccount

# from models.contractor_bank_account import ContractorBankAccount
from models.client_bank_account import ClientBankAccount
from models.supplier_bank_account import SupplierBankAccount
from models.employee_bank_account import EmployeeBankAccount

# from models.project import Project
# from models.project_transaction import ProjectTransaction

from models.bank_account import BankAccount
from models.bank_account_transaction import BankAccountTransaction
from models.bank_account_transfer import BankAccountTransfer


class MapBankAccounts(object):

    def __init__(self):
        pass

    def init(self, mapper):
        mapper.connect(
            "get_bank_accounts",
            "/catalog/{associated_with}/{associated_id}/bank-accounts",
            controller=self,
            action="get_bank_accounts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_bank_accounts",
            "/bank-accounts",
            controller=self,
            action="get_bank_accounts",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_bank_account_by_id",
            "/catalog/{associated_with}/{associated_id}/bank-account/{bank_account_id}",
            controller=self,
            action="get_bank_account_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_bank_account",
            "/catalog/{associated_with}/{associated_id}/bank-account/{bank_account_id}",
            controller=self,
            action="save_bank_account",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "patch_bank_account",
            "/catalog/{associated_with}/{associated_id}/bank-account/{bank_account_id}",
            controller=self,
            action="patch_bank_account",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "delete_bank_account",
            "/catalog/{associated_with}/{associated_id}/bank-account/{bank_account_id}",
            controller=self,
            action="delete_bank_account",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_bank_account_transactions",
            "/{associated_with}/{associated_id}/bank-account/{bank_account_id}/transactions",
            controller=self,
            action="get_bank_account_transactions",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_bank_account_transaction",
            "/{associated_with}/{associated_id}/bank-account/{bank_account_id}/transaction/{transaction_id}",
            controller=self,
            action="save_bank_account_transaction",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_bank_account_transfers",
            "/bank-account-transfers",
            controller=self,
            action="get_bank_account_transfers",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_bank_account_transfer",
            "/bank-account-transfer/{transfer_id}",
            controller=self,
            action="save_bank_account_transfer",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "tool_fix_transactions_balance",
            "/tool/fix-bank-account-transactions-balance",
            controller=self,
            action="tool_fix_transactions_balance",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_bank_accounts(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        associated_with = kwargs.get("associated_with")
        associated_id = kwargs.get("associated_id")
        filters = kwargs.get("filters", "[]")

        look_for_criterias = [
            {"code": look_for, "op": "like"},
            {"bank_code": look_for, "op": "like"},
            {"bank_name": look_for, "op": "like"},
            {"description": look_for, "op": "like"},
            {"account_number": look_for, "op": "like"},
            {"interbank_key": look_for, "op": "like"},
        ]

        if len(look_for) > 0:
            try:
                """Insert the phases"""
                tmp = json.loads(filters)
            except Exception:
                raise cherrypy.HTTPError(400, "Incorrect format/value for `filters`")

            for filter in tmp:
                if filter["filter_by"] == "associated_with":
                    for type in filter["value"]:
                        look_for_criterias.append(
                            {
                                "associated_id": HelperAccountRelation.get_subquery_sql(type=type, look_for=look_for),
                                "op": "in",
                            }
                        )

        criterias = [_OR(*look_for_criterias)]

        if associated_with:
            criterias.append({"associated_with": associated_with})

        if associated_id:
            criterias.append({"associated_id": associated_id})

        criterias = criterias + Utils().convert_filters(filters, force_status=True)

        conn = BankAccount().get_connection()
        query = Query(model=BankAccount())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for item in result["results"]:

            item["relation"] = HelperAccountRelation.get(
                type=item["associated_with"], id=item["associated_id"], as_dict=True, conn=conn
            )

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_bank_account_by_id(self, **kwargs):

        # Get body content
        associated_with = kwargs.get("associated_with")
        associated_id = kwargs.get("associated_id")
        bank_account_id = kwargs.get("bank_account_id")

        criterias = [{"bank_account_id": bank_account_id}]

        if associated_with != "generic":
            criterias.append(
                {"associated_with": associated_with},
            )

        if associated_id != "generic":
            criterias.append(
                {"associated_id": associated_id},
            )

        conn = BankAccount().get_connection()
        bank_account = BankAccount().where(*criterias).one_or_none(conn=conn)

        if bank_account is None:
            raise cherrypy.HTTPError(404, "Not Found")

        bank_account = bank_account.as_dict()
        bank_account["relation"] = HelperAccountRelation.get(
            type=bank_account["associated_with"], id=bank_account["associated_id"], as_dict=True, conn=conn
        )

        return bank_account

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "associated_with",
            "internal_code",
            "bank_id",
            "bank_code",
            "bank_name",
            "description",
            "currency",
            "account_number",
            "card_number",
            "interbank_key",
            "reference",
            "is_default",
            "status",
        ]
    )
    def save_bank_account(self, **kwargs):

        # Get body content
        body = cherrypy.request.json
        associated_with = body.get("associated_with")
        associated_id = body.get("associated_id")
        bank_account_id = body.get("bank_account_id")

        conn = BankAccount().get_connection()
        account = (
            BankAccount()
            .where(
                {"associated_with": associated_with},
                {"associated_id": associated_id},
                {"bank_account_id": bank_account_id},
            )
            .one_or_none(conn=conn)
        )

        try:
            conn.begin(conn)

            # disable previus default if marked
            if body.get("is_default") == 1:
                sql = (
                    """
                        UPDATE `{table}`
                        SET
                            `is_default` = 0
                        WHERE
                            `associated_with` = %s AND
                            `associated_id` = %s AND
                            `is_default` = 1
                    """
                ).format(table=BankAccount()._TABLE)

                args = [associated_with, associated_id]
                conn.execute(sql, *args, connection=None)

            is_new = False
            if account is None:
                is_new = True
                body["code"] = Serie.generate(
                    reference="{}_{}".format(associated_with, associated_id), key="bank_accounts", conn=conn
                )
                account = BankAccount()
                account.balance = 0
                account.created_at = datetime.utcnow()

            account.set_attrs(body)
            account.updated_at = datetime.utcnow()
            account.insert(conn=conn) if is_new else account.update(conn=conn)

            if is_new and associated_with == "company":
                relation = CompanyBankAccount()
                relation.company_id = associated_id
                relation.bank_account_id = bank_account_id
                relation.created_at = datetime.utcnow()
                relation.updated_at = datetime.utcnow()
                relation.insert(conn=conn)

            # elif is_new and associated_with == 'contractor':
            #     relation = ContractorBankAccount()
            #     relation.contractor_id = associated_id
            #     relation.bank_account_id = bank_account_id
            #     relation.created_at = datetime.utcnow()
            #     relation.updated_at = datetime.utcnow()
            #     relation.insert(conn=conn)

            elif is_new and associated_with == "client":
                relation = ClientBankAccount()
                relation.client_id = associated_id
                relation.bank_account_id = bank_account_id
                relation.created_at = datetime.utcnow()
                relation.updated_at = datetime.utcnow()
                relation.insert(conn=conn)

            elif is_new and associated_with == "supplier":
                relation = SupplierBankAccount()
                relation.supplier_id = associated_id
                relation.bank_account_id = bank_account_id
                relation.created_at = datetime.utcnow()
                relation.updated_at = datetime.utcnow()
                relation.insert(conn=conn)

            elif is_new and associated_with == "employee":
                relation = EmployeeBankAccount()
                relation.employee_id = associated_id
                relation.bank_account_id = bank_account_id
                relation.created_at = datetime.utcnow()
                relation.updated_at = datetime.utcnow()
                relation.insert(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))
        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured(["admin"])
    def patch_bank_account(self, **kwargs):
        token = kwargs.get("token")

        # Get body content
        body = cherrypy.request.json
        bank_account_id = body.get("bank_account_id")

        conn = BankAccount().get_connection()
        account = BankAccount().where({"bank_account_id": bank_account_id}).one_or_none(conn=conn)

        if account is None:
            raise cherrypy.HTTPError(404, "Not Found")

        user_employee = UserEmployee().fields(["employee_id"]).where({"user_id": token.user_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            # optional values
            attrs = ["balance"]
            for key, value in body.items():
                if key in attrs:
                    setattr(account, key, value)
            account.update(conn=conn)

            event = BankAccountTransaction()
            event.bank_account_id = account.bank_account_id
            event.transaction_id = str(uuid.uuid4())
            event.relation_id = user_employee.employee_id
            event.relation_type = "employee"
            event.user_id = token.user_id
            event.code = Serie.generate(
                reference="bank-account-transactions", key=account.bank_account_id, zfill=6, conn=conn
            )

            event.type = "set-balance"
            event.transaction_date = datetime.utcnow()
            event.amount = account.balance
            event.balance = account.balance
            event.notes = ""
            event.status = "active"
            event.created_at = datetime.utcnow()
            event.updated_at = datetime.utcnow()
            event.insert(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem saving data: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_bank_account(self, **kwargs):

        # Get kwargs content
        associated_with = kwargs.get("associated_with")
        associated_id = kwargs.get("associated_id")
        bank_account_id = kwargs.get("bank_account_id")

        conn = BankAccount().get_connection()
        account = (
            BankAccount()
            .where(
                {"associated_with": associated_with},
                {"associated_id": associated_id},
                {"bank_account_id": bank_account_id},
            )
            .one_or_none(conn=conn)
        )

        if account is None:
            raise cherrypy.HTTPError(404, "Not Found")

        if account.balance > 0:
            raise cherrypy.HTTPError(423, "Locked")

        account.status = "inactive"
        account.updated_at = datetime.utcnow()
        account.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_bank_account_transactions(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        bank_account_id = kwargs.get("bank_account_id", 0)
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"bank_account_id": bank_account_id},
            _OR({"code": look_for, "op": "like"}, {"amount": look_for}),
            _AND({"transaction_date": start_date, "op": "gte"}, {"transaction_date": end_date, "op": "lte"}),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = BankAccountTransaction().get_connection()
        query = Query(model=BankAccountTransaction())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(
            [
                "-transaction_date",
                "-code",
            ]
        )

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for item in result["results"]:
            item["user"] = User().where({"user_id": item["user_id"]}).one_or_none(conn=conn).as_dict()

            # if item['relation_type'] == 'project':
            #     item['relation'] = (
            #         Project()
            #         .where({
            #             'project_id': (
            #                 ProjectTransaction()
            #                 .fields(['project_id'])
            #                 .where(
            #                     {'transaction_id': item['transaction_id']}
            #                 )
            #                 .sql(
            #                     remove_offset_limit = True
            #                 )
            #             ),
            #             'op': 'in'

            #         }).one_or_none(
            #             conn=conn
            #         ).as_dict()
            #     )
            # else:
            item["relation"] = HelperAccountRelation.get(
                type=item["relation_type"], id=item["relation_id"], as_dict=True, conn=conn
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured(["admin"])
    @tools.validate_body_params(
        [
            "associated_with",
            "associated_id",
            "bank_account_id",
            "transaction_id",
            "type",
            "transaction_date",
            "amount",
            "notes",
        ]
    )
    def save_bank_account_transaction(self, **kwargs):
        token = kwargs.get("token")

        # Get body content
        body = cherrypy.request.json
        bank_account_id = body.get("bank_account_id")
        transaction_id = body.get("transaction_id")

        type = body.get("type")
        transaction_date = body.get("transaction_date")
        amount = body.get("amount")
        notes = body.get("notes")

        conn = BankAccountTransaction().get_connection()
        user_employee = UserEmployee().fields(["employee_id"]).where({"user_id": token.user_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            # Affect bank account
            account = BankAccount().where({"bank_account_id": bank_account_id}).one_or_none(conn=conn)

            if type == "deposit":
                account.balance = account.balance + amount
            else:
                account.balance = account.balance - amount

            account.updated_at = datetime.utcnow()
            account.update(conn=conn)

            event = BankAccountTransaction()
            event.bank_account_id = account.bank_account_id
            event.transaction_id = transaction_id
            event.relation_id = user_employee.employee_id
            event.relation_type = "employee"
            event.user_id = token.user_id
            event.code = Serie.generate(
                reference="bank-account-transactions", key=account.bank_account_id, zfill=6, conn=conn
            )

            event.type = type
            event.transaction_date = transaction_date
            event.amount = amount
            event.balance = account.balance
            event.notes = notes
            event.status = "active"
            event.created_at = datetime.utcnow()
            event.updated_at = datetime.utcnow()
            event.insert(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem adding item: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_bank_account_transfers(self, **kwargs):

        result = {}
        result["results"] = []
        result["total_rows"] = 0

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 50)
        look_for = kwargs.get("look_for", "")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        filters = kwargs.get("filters", "[]")

        criterias = [
            {"transaction_date": start_date, "op": "gte"},
            {"transaction_date": end_date, "op": "lte"},
            _OR({"code": look_for, "op": "like"}, {"amount": look_for}),
        ]

        criterias = criterias + Utils().convert_filters(filters)

        conn = BankAccountTransfer().get_connection()
        query = Query(model=BankAccountTransfer())
        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["-code"])

        result["results"] = query.all(conn=conn, collection=False)
        result["total_rows"] = query.count(conn=conn)

        for item in result["results"]:
            item["user"] = User().where({"user_id": item["user_id"]}).one_or_none(conn=conn).as_dict()

            item["relation"] = HelperAccountRelation.get(
                type=item["relation_type"], id=item["relation_id"], as_dict=True, conn=conn
            )

            item["from_account"] = (
                BankAccount().where({"bank_account_id": item["from_account_id"]}).one_or_none(conn=conn).as_dict()
            )
            item["from_account"]["relation"] = HelperAccountRelation.get(
                type=item["from_account"]["associated_with"],
                id=item["from_account"]["associated_id"],
                as_dict=True,
                conn=conn,
            )

            item["to_account"] = (
                BankAccount().where({"bank_account_id": item["to_account_id"]}).one_or_none(conn=conn).as_dict()
            )
            item["to_account"]["relation"] = HelperAccountRelation.get(
                type=item["to_account"]["associated_with"],
                id=item["to_account"]["associated_id"],
                as_dict=True,
                conn=conn,
            )

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured(["admin"])
    @tools.validate_body_params(
        ["transfer_id", "from_account_id", "to_account_id", "transaction_date", "amount", "notes"]
    )
    def save_bank_account_transfer(self, **kwargs):
        token = kwargs.get("token")

        # Get body content
        body = cherrypy.request.json
        transfer_id = body.get("transfer_id")
        amount = body.get("amount")

        conn = BankAccountTransfer().get_connection()

        # Affect bank account
        from_account = BankAccount().where({"bank_account_id": body.get("from_account_id")}).one_or_none(conn=conn)

        to_account = BankAccount().where({"bank_account_id": body.get("to_account_id")}).one_or_none(conn=conn)

        if from_account.balance < amount:
            raise cherrypy.HTTPError(406, "Not Aceptable")

        user_employee = UserEmployee().fields(["employee_id"]).where({"user_id": token.user_id}).one_or_none(conn=conn)

        try:
            conn.begin(conn)

            transfer = BankAccountTransfer()
            transfer.code = Serie.generate(reference="bank-account-transfers", key="transfers", zfill=6, conn=conn)
            transfer.set_attrs(body)
            transfer.user_id = token.user_id
            transfer.relation_id = user_employee.employee_id
            transfer.relation_type = "employee"
            transfer.status = "active"
            transfer.created_at = datetime.utcnow()
            transfer.updated_at = datetime.utcnow()
            transfer.insert(conn=conn)

            from_account.balance = from_account.balance - transfer.amount
            from_account.updated_at = datetime.utcnow()
            from_account.update(conn=conn)

            event = BankAccountTransaction()
            event.bank_account_id = from_account.bank_account_id
            event.transaction_id = transfer_id
            event.relation_id = user_employee.employee_id
            event.relation_type = "employee"
            event.user_id = token.user_id
            event.code = Serie.generate(
                reference="bank-account-transactions", key=from_account.bank_account_id, zfill=6, conn=conn
            )

            event.type = "withdrawal"
            event.transaction_date = transfer.transaction_date
            event.amount = transfer.amount
            event.balance = from_account.balance
            event.notes = transfer.notes
            event.status = "active"
            event.created_at = datetime.utcnow()
            event.updated_at = datetime.utcnow()
            event.insert(conn=conn)

            to_account.balance = to_account.balance + transfer.amount
            to_account.updated_at = datetime.utcnow()
            to_account.update(conn=conn)

            event = BankAccountTransaction()
            event.bank_account_id = to_account.bank_account_id
            event.transaction_id = transfer_id
            event.relation_id = user_employee.employee_id
            event.relation_type = "employee"
            event.user_id = token.user_id
            event.code = Serie.generate(
                reference="bank-account-transactions", key=to_account.bank_account_id, zfill=6, conn=conn
            )

            event.type = "deposit"
            event.transaction_date = transfer.transaction_date
            event.amount = transfer.amount
            event.balance = to_account.balance
            event.notes = transfer.notes
            event.status = "active"
            event.created_at = datetime.utcnow()
            event.updated_at = datetime.utcnow()
            event.insert(conn=conn)

            conn.commit(conn)
        except pymysql.err.IntegrityError as e:
            conn.rollback(conn)
            raise cherrypy.HTTPError(409, str(e))
        except Exception as e:
            # Rollback changes
            conn.rollback(conn)
            raise cherrypy.HTTPError(500, "Problem adding item: {}".format(str(e)))

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured(["admin"])
    def tool_fix_transactions_balance(self, **kwargs):

        conn = BankAccount().get_connection()
        try:
            # Get bank accounts
            accounts = conn.execute(
                """
                    SELECT *
                    FROM
                        `bank_accounts`
                    ORDER BY
                        `created_at`
                """,
                log_actions=False,
            )

            for account in accounts:
                transactions = conn.execute(
                    """
                        SELECT *
                        FROM
                            `bank_accounts_transactions`
                        WHERE
                            `bank_account_id` = %s
                        ORDER BY `transaction_date` , `code`
                    """,
                    *[account["bank_account_id"]],
                    log_actions=False
                )

                balance = 0
                for transaction in transactions:
                    if transaction["status"] == "inactive":
                        continue

                    if transaction["type"] == "set-balance":
                        balance = transaction["balance"]
                    elif transaction["type"] in ["expense", "withdrawal", "reimbursement"]:
                        balance -= transaction["amount"]
                    elif transaction["type"] in ["income", "deposit", "refund"]:
                        balance += transaction["amount"]

                    if balance != transaction["balance"]:
                        logging.info(
                            "Type {}, Amount {}, Balance {}, New Balance {}".format(
                                transaction["type"], transaction["amount"], transaction["balance"], balance
                            )
                        )
                        transaction["balance"] = balance

                        conn.execute(
                            """
                                UPDATE
                                `bank_accounts_transactions`
                                SET
                                `balance` = %s
                                WHERE
                                `bank_account_id` = %s AND
                                `transaction_id` = %s
                            """,
                            *[transaction["balance"], transaction["bank_account_id"], transaction["transaction_id"]],
                            log_actions=False
                        )

                if balance != account["balance"]:
                    logging.info("Final balance {}, current balance {}".format(balance, account["balance"]))
                    account["balance"] = balance

                    conn.execute(
                        """
                            UPDATE
                            `bank_accounts`
                            SET
                            `balance` = %s
                            WHERE
                            `bank_account_id` = %s
                        """,
                        *[account["balance"], account["bank_account_id"]],
                        log_actions=False
                    )

            # conn.commit()
        except Exception as e:
            logging.error("DataBase Error: {}".format(str(e)))

        return True
