import json
import uuid
import cherrypy
import traceback

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pytz import timezone


from utils.decorators import tools
from utils.convert import Convert
from utils.query import _OR
from helpers.notification import Notification

from models.branch_office_warehouse import BranchOfficeWarehouse
from models.shopping_cart import ShoppingCart
from models.shopping_cart_item import ShoppingCartItem
from models.shopping_cart_item_tax import ShoppingCartItemTax

from models.state import State
from models.municipality import Municipality
from models.measure import Measure

from models.warehouse import Warehouse
from models.client import Client
from models.product import Product
from models.product_tax import ProductTax
from models.measure import Measure
from models.tax import Tax
from models.stock import Stock
from models.product_tax import ProductTax
from models.tax import Tax
from views.product_measure import vProductMeasure

from models.serie import Serie
from models.company import Company
from models.branch_office import BranchOffice
from models.user_employee import UserEmployee
from models.employee import Employee


from models.postal_code import PostalCode
from models.sale_document import SaleDocument
from models.sale_document_product import SaleDocumentProduct
from models.sale_document_tax import SaleDocumentTax
from models.delivery_address import DeliveryAddress
from models.document_payment import DocumentPayment


class MapShoppingCart(object):

    DEFAULT_CURRENCY = "mxn"
    DEFAULT_EXCHANGE_RATE = Decimal("1")
    CART_EXPIRATION_DAYS = 30

    ECOMMERCE_PAYMENT_METHOD = "31"
    ECOMMERCE_PAYMENT_TYPE = "PUE"
    ECOMMERCE_FISCAL_USE = "G03"

    SHIPPING_FREE_MINIMUM = Decimal("2500.00")
    SHIPPING_PRICE = Decimal("130.00")

    # Replace these two values with the service product.
    SHIPPING_PRODUCT_ID = "2748181b-8b4f-4b55-986e-48c50e4f827e"
    SHIPPING_MEASURE_ID = "cc71d0c9-2fdf-434d-90b1-4e5228d0d6c3"

    def __init__(self):
        pass

    def init(self, mapper=None):

        mapper.connect(
            "get_shopping_cart",
            "/shopping-cart",
            controller=self,
            action="get_shopping_cart",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "create_shopping_cart",
            "/shopping-cart",
            controller=self,
            action="create_shopping_cart",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "clear_shopping_cart",
            "/shopping-cart",
            controller=self,
            action="clear_shopping_cart",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "shopping_cart_add_item",
            "/shopping-cart/items",
            controller=self,
            action="shopping_cart_add_item",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "shopping_cart_update_item",
            "/shopping-cart/items/{cart_item_id}",
            controller=self,
            action="shopping_cart_update_item",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "shopping_cart_delete_item",
            "/shopping-cart/items/{cart_item_id}",
            controller=self,
            action="shopping_cart_delete_item",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "checkout_shopping_cart",
            "/shopping-cart/checkout",
            controller=self,
            action="checkout_shopping_cart",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

    # -------------------------------------------------------------------------
    # CART
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_shopping_cart(self, **kwargs):

        token = kwargs.get("token")
        conn = ShoppingCart().get_connection()

        cart_token = self.__get_cart_token()

        cart = self.__get_active_cart(
            cart_token=cart_token,
            conn=conn,
        )

        if cart is None:
            raise cherrypy.HTTPError(404, "Shopping cart not found")

        return self.__serialize_cart(
            cart=cart,
            conn=conn,
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "branch_id",
            "warehouse_id",
            "client_id",
        ]
    )
    def create_shopping_cart(self, **kwargs):

        token = kwargs.get("token")

        body = cherrypy.request.json
        print(body)

        branch_id = body.get("branch_id")
        warehouse_id = body.get("warehouse_id")
        client_id = body.get("client_id")

        currency = str(body.get("currency", self.DEFAULT_CURRENCY)).lower()

        exchange_rate = self.__decimal(body.get("exchange_rate", self.DEFAULT_EXCHANGE_RATE))

        conn = ShoppingCart().get_connection()

        self.__validate_cart_context(
            branch_id=branch_id,
            warehouse_id=warehouse_id,
            client_id=client_id,
            conn=conn,
        )

        try:
            conn.begin(conn)

            cart_token = self.__get_cart_token()
            existing_cart = self.__get_active_cart(
                cart_token=cart_token,
                conn=conn,
            )

            if existing_cart is not None:

                same_context = (
                    existing_cart.branch_id == branch_id
                    and existing_cart.warehouse_id == warehouse_id
                    and existing_cart.client_id == client_id
                    and existing_cart.currency == currency
                )

                if same_context:
                    conn.commit(conn)

                    cherrypy.response.status = 200

                    return self.__serialize_cart(
                        cart=existing_cart,
                        conn=conn,
                    )

                existing_cart.status = "abandoned"
                existing_cart.updated_at = datetime.utcnow()
                existing_cart.update(conn=conn)

            now = datetime.utcnow()

            cart = ShoppingCart()
            cart.cart_id = str(uuid.uuid4())
            cart.cart_token = cart_token

            cart.branch_id = branch_id
            cart.warehouse_id = warehouse_id
            cart.client_id = client_id
            cart.user_id = token.user_id

            cart.currency = currency
            cart.exchange_rate = exchange_rate

            cart.status = "active"
            cart.expires_at = now + timedelta(days=self.CART_EXPIRATION_DAYS)

            cart.created_at = now
            cart.updated_at = now

            cart.insert(conn=conn)

            conn.commit(conn)

        except cherrypy.HTTPError:
            conn.rollback(conn)
            raise

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem creating shopping cart: {}".format(error),
            )

        cherrypy.response.status = 201

        return self.__serialize_cart(
            cart=cart,
            conn=conn,
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def clear_shopping_cart(self, **kwargs):

        token = kwargs.get("token")
        conn = ShoppingCart().get_connection()

        cart_token = self.__get_cart_token()
        cart = self.__get_active_cart(
            cart_token=cart_token,
            conn=conn,
        )

        if cart is None:
            cherrypy.response.status = 204
            return None

        try:
            conn.begin(conn)

            cart.delete(
                hard_delete=True,
                conn=conn,
            )

            conn.commit(conn)

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem clearing shopping cart: {}".format(error),
            )

        cherrypy.response.status = 204
        return None

    # -------------------------------------------------------------------------
    # ITEMS
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "product_id",
            "measure_id",
            "quantity",
        ]
    )
    def shopping_cart_add_item(self, **kwargs):

        token = kwargs.get("token")
        body = cherrypy.request.json

        product_id = body.get("product_id")
        measure_id = body.get("measure_id")
        quantity = self.__decimal(body.get("quantity"))

        if quantity <= 0:
            raise cherrypy.HTTPError(
                400,
                "Quantity must be greater than zero",
            )

        conn = ShoppingCart().get_connection()

        cart_token = self.__get_cart_token()
        cart = self.__get_active_cart(
            cart_token=cart_token,
            conn=conn,
        )

        if cart is None:
            raise cherrypy.HTTPError(
                404,
                "Shopping cart not found",
            )

        warehouse_product = self.__get_warehouse_product(
            warehouse_id=cart.warehouse_id,
            product_id=product_id,
            measure_id=measure_id,
            conn=conn,
        )

        try:
            conn.begin(conn)

            item = (
                ShoppingCartItem()
                .where(
                    {"cart_id": cart.cart_id},
                    {"product_id": warehouse_product["product_id"]},
                    {"measure_id": measure_id},
                )
                .one_or_none(conn=conn)
            )

            now = datetime.utcnow()

            if item is None:
                item = ShoppingCartItem()
                item.cart_item_id = str(uuid.uuid4())
                item.cart_id = cart.cart_id
                item.product_id = warehouse_product["product_id"]
                item.measure_id = measure_id
                item.quantity = Decimal("0")
                item.created_at = now

            new_quantity = self.__decimal(item.quantity) + quantity

            measure = warehouse_product["measure"]

            pricing = self.__calculate_item_pricing(
                quantity=new_quantity,
                price=measure["price"],
                discount_percent=measure["discount"],
            )

            item.equivalence = self.__decimal(measure.get("equivalence", 1))

            item.quantity = new_quantity
            item.currency = cart.currency

            item.original_price = pricing["original_price"]
            item.unit_price = pricing["unit_price"]
            item.discount_amount = pricing["discount_amount"]

            item.updated_at = now

            item.update_or_insert(conn=conn)

            self.__save_item_taxes(
                cart_item=item,
                taxes=warehouse_product["taxes"],
                conn=conn,
            )

            cart.updated_at = now
            cart.update(conn=conn)

            conn.commit(conn)

        except cherrypy.HTTPError:
            conn.rollback(conn)
            raise

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem adding shopping cart item: {}".format(error),
            )

        return self.__serialize_cart(
            cart=cart,
            conn=conn,
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "quantity",
        ]
    )
    def shopping_cart_update_item(self, cart_item_id=None, **kwargs):

        token = kwargs.get("token")
        body = cherrypy.request.json

        quantity = self.__decimal(body.get("quantity"))

        if quantity < 0:
            raise cherrypy.HTTPError(
                400,
                "Quantity cannot be negative",
            )

        conn = ShoppingCart().get_connection()

        cart_token = self.__get_cart_token()
        cart = self.__get_active_cart(
            cart_token=cart_token,
            conn=conn,
        )

        if cart is None:
            raise cherrypy.HTTPError(
                404,
                "Shopping cart not found",
            )

        item = (
            ShoppingCartItem()
            .where(
                {"cart_item_id": cart_item_id},
                {"cart_id": cart.cart_id},
            )
            .one_or_none(conn=conn)
        )

        if item is None:
            raise cherrypy.HTTPError(
                404,
                "Shopping cart item not found",
            )

        try:
            conn.begin(conn)

            if quantity == 0:
                item.delete(
                    hard_delete=True,
                    conn=conn,
                )

            else:
                warehouse_product = self.__get_warehouse_product(
                    warehouse_id=cart.warehouse_id,
                    product_id=item.product_id,
                    measure_id=item.measure_id,
                    conn=conn,
                )

                measure = warehouse_product["measure"]

                pricing = self.__calculate_item_pricing(
                    quantity=quantity,
                    price=measure["price"],
                    discount_percent=measure["discount"],
                )

                item.equivalence = self.__decimal(measure.get("equivalence", 1))

                item.quantity = quantity
                item.currency = cart.currency
                item.original_price = pricing["original_price"]
                item.unit_price = pricing["unit_price"]
                item.discount_amount = pricing["discount_amount"]
                item.updated_at = datetime.utcnow()

                item.update(conn=conn)

                self.__save_item_taxes(
                    cart_item=item,
                    taxes=warehouse_product["taxes"],
                    conn=conn,
                )

            cart.updated_at = datetime.utcnow()
            cart.update(conn=conn)

            conn.commit(conn)

        except cherrypy.HTTPError:
            conn.rollback(conn)
            raise

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem updating shopping cart item: {}".format(error),
            )

        return self.__serialize_cart(
            cart=cart,
            conn=conn,
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def shopping_cart_delete_item(self, cart_item_id=None, **kwargs):

        token = kwargs.get("token")
        conn = ShoppingCart().get_connection()

        cart_token = self.__get_cart_token()
        cart = self.__get_active_cart(
            cart_token=cart_token,
            conn=conn,
        )

        if cart is None:
            raise cherrypy.HTTPError(
                404,
                "Shopping cart not found",
            )

        item = (
            ShoppingCartItem()
            .where(
                {"cart_item_id": cart_item_id},
                {"cart_id": cart.cart_id},
            )
            .one_or_none(conn=conn)
        )

        if item is None:
            raise cherrypy.HTTPError(
                404,
                "Shopping cart item not found",
            )

        try:
            conn.begin(conn)

            item.delete(
                hard_delete=True,
                conn=conn,
            )

            cart.updated_at = datetime.utcnow()
            cart.update(conn=conn)

            conn.commit(conn)

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem deleting shopping cart item: {}".format(error),
            )

        return self.__serialize_cart(
            cart=cart,
            conn=conn,
        )

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "payment",
            "delivery_address",
        ]
    )
    def checkout_shopping_cart(self, **kwargs):

        token = kwargs.get("token")
        cart_token = self.__get_cart_token()

        body = cherrypy.request.json

        user_id = token.user_id
        payment_body = body.get("payment", {})
        address_body = body.get("delivery_address", {})

        conn = ShoppingCart().get_connection()
        user_employee = (
            UserEmployee()
            .where(
                {"user_id": user_id},
            )
            .one_or_none(conn=conn)
        )

        if user_employee is None:
            raise cherrypy.HTTPError(
                500,
                "User is not associated with an employee",
            )

        employee = (
            Employee()
            .where(
                {"employee_id": user_employee.employee_id},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if employee is None:
            raise cherrypy.HTTPError(
                500,
                "Employee not found or inactive",
            )

        company_id = employee.company_id
        seller_id = employee.employee_id

        provider = str(payment_body.get("provider", "")).strip().lower()

        provider_order_id = str(payment_body.get("provider_order_id", "")).strip()

        provider_transaction_id = str(
            payment_body.get(
                "provider_transaction_id",
                "",
            )
        ).strip()

        provider_status = str(payment_body.get("provider_status", "")).strip().upper()

        captured_amount = self.__money(payment_body.get("amount", 0))

        captured_currency = str(payment_body.get("currency", "")).strip().lower()

        if provider not in ["paypal", "mercado_pago"]:
            raise cherrypy.HTTPError(
                400,
                "Invalid payment provider",
            )

        if not provider_order_id:
            raise cherrypy.HTTPError(
                400,
                "Missing PayPal order ID",
            )

        if not provider_transaction_id:
            raise cherrypy.HTTPError(
                400,
                "Missing PayPal transaction ID",
            )

        if provider_status != "COMPLETED":
            raise cherrypy.HTTPError(
                409,
                "PayPal payment is not completed",
            )

        required_address_fields = [
            "name",
            "email",
            "phone",
            "street",
            "exterior_number",
            "neighborhood",
            "postal_code",
        ]

        for field in required_address_fields:
            if not str(address_body.get(field, "")).strip():
                raise cherrypy.HTTPError(
                    400,
                    "Missing delivery address field: {}".format(field),
                )

        phone = "".join(character for character in str(address_body.get("phone", "")) if character.isdigit())

        if phone.startswith("52") and len(phone) == 12:
            phone = phone[2:]

        if len(phone) != 10:
            raise cherrypy.HTTPError(
                400,
                "Phone must contain 10 digits",
            )

        zip_code = str(address_body.get("postal_code", "")).strip()

        if len(zip_code) != 5 or not zip_code.isdigit():
            raise cherrypy.HTTPError(
                400,
                "Invalid postal code",
            )

        try:
            conn.begin(conn)

            cart = self.__get_active_cart(
                cart_token=cart_token,
                conn=conn,
            )

            if cart is None:
                raise cherrypy.HTTPError(
                    404,
                    "Shopping cart not found",
                )

            document_id = cart.cart_id

            # -------------------------------------
            # Idempotency by cart/document ID
            # -------------------------------------

            existing_document = (
                SaleDocument()
                .where(
                    {
                        "document_id": document_id,
                    }
                )
                .one_or_none(conn=conn)
            )

            if existing_document is not None:
                existing_payment = (
                    DocumentPayment()
                    .where(
                        {
                            "document_id": document_id,
                        }
                    )
                    .one_or_none(conn=conn)
                )

                conn.rollback(conn)

                return {
                    "document_id": existing_document.document_id,
                    "code": existing_document.code,
                    "payment_id": (existing_payment.payment_id if existing_payment else None),
                    "payment_code": (existing_payment.code if existing_payment else None),
                    "payment_status": existing_document.payment_status,
                    "total": float(existing_document.total),
                    "currency": existing_document.currency,
                    "already_processed": True,
                }

            # -------------------------------------
            # Idempotency by PayPal capture ID
            # -------------------------------------

            existing_payment = (
                DocumentPayment()
                .where(
                    {"provider": provider},
                    {
                        "provider_transaction_id": provider_transaction_id,
                    },
                    {"status": "active"},
                )
                .one_or_none(conn=conn)
            )

            if existing_payment is not None:
                previous_document = (
                    SaleDocument()
                    .where(
                        {
                            "document_id": existing_payment.document_id,
                        }
                    )
                    .one_or_none(conn=conn)
                )

                conn.rollback(conn)

                return {
                    "document_id": previous_document.document_id,
                    "code": previous_document.code,
                    "payment_id": existing_payment.payment_id,
                    "payment_code": existing_payment.code,
                    "payment_status": previous_document.payment_status,
                    "total": float(previous_document.total),
                    "currency": previous_document.currency,
                    "already_processed": True,
                }

            # -------------------------------------
            # Load cart items
            # -------------------------------------

            cart_items = (
                ShoppingCartItem()
                .where(
                    {
                        "cart_id": cart.cart_id,
                    }
                )
                .all(
                    conn=conn,
                    collection=False,
                )
            )

            if not cart_items:
                raise cherrypy.HTTPError(
                    400,
                    "Shopping cart is empty",
                )

            company = (
                Company()
                .where(
                    {
                        "company_id": company_id,
                    }
                )
                .one_or_none(conn=conn)
            )

            if company is None:
                raise cherrypy.HTTPError(
                    500,
                    "Invalid ecommerce company",
                )

            branch = (
                BranchOffice()
                .where(
                    {
                        "branch_id": cart.branch_id,
                    }
                )
                .one_or_none(conn=conn)
            )

            if branch is None:
                raise cherrypy.HTTPError(
                    500,
                    "Invalid cart branch",
                )

            # -------------------------------------
            # Recalculate products
            # -------------------------------------

            sale_details = []

            products_amount = Decimal("0.00")
            products_subtotal = Decimal("0.00")
            products_discount = Decimal("0.00")
            products_taxes = Decimal("0.00")
            products_total = Decimal("0.00")

            for cart_item in cart_items:

                quantity = self.__money(cart_item["quantity"])

                original_price = self.__money(cart_item["original_price"])

                unit_price = self.__money(cart_item["unit_price"])

                discount_amount = self.__money(cart_item["discount_amount"])

                amount = self.__money(original_price * quantity)

                subtotal = self.__money(unit_price * quantity)

                item_taxes = (
                    ShoppingCartItemTax()
                    .where(
                        {
                            "cart_item_id": cart_item["cart_item_id"],
                        }
                    )
                    .all(
                        conn=conn,
                        collection=False,
                    )
                )

                tax_total = self.__money(sum(Decimal(str(item.get("tax_amount", 0))) for item in item_taxes))

                # Current cart totals are tax-inclusive.
                total = subtotal

                discount_factor = Decimal("0.00")

                if amount > 0:
                    discount_factor = self.__money(discount_amount / amount)

                sale_details.append(
                    {
                        "product_id": cart_item["product_id"],
                        "measure_id": cart_item["measure_id"],
                        "currency": cart_item["currency"],
                        "quantity": quantity,
                        "original_price": original_price,
                        "discount_factor": discount_factor,
                        "price": unit_price,
                        "amount": amount,
                        "subtotal": subtotal,
                        "discount": discount_amount,
                        "taxes": tax_total,
                        "total": total,
                        "tax_rows": item_taxes,
                    }
                )

                products_amount += amount
                products_subtotal += subtotal
                products_discount += discount_amount
                products_taxes += tax_total
                products_total += total

            # -------------------------------------
            # Shipping service
            # -------------------------------------

            shipping_amount = Decimal("0.00") if products_total >= self.SHIPPING_FREE_MINIMUM else self.SHIPPING_PRICE

            shipping_product = (
                Product()
                .where(
                    {
                        "product_id": self.SHIPPING_PRODUCT_ID,
                    },
                    # {"status": "active"},
                )
                .one_or_none(conn=conn)
            )

            if shipping_product is None:
                raise cherrypy.HTTPError(
                    500,
                    "Shipping service product not found",
                )

            shipping_tax_rows = (
                ProductTax()
                .where(
                    {
                        "product_id": self.SHIPPING_PRODUCT_ID,
                    },
                    {"status": "active"},
                )
                .all(
                    conn=conn,
                    collection=False,
                )
            )

            shipping_tax_total = Decimal("0.00")

            for tax_row in shipping_tax_rows:
                percent = Decimal(str(tax_row.get("percent", 0)))

                # Shipping price is treated as tax-inclusive,
                # matching the current shopping-cart convention.
                if percent > 0 and shipping_amount > 0:
                    tax_amount = self.__money(
                        shipping_amount - (shipping_amount / (Decimal("1.00") + (percent / Decimal("100.00"))))
                    )
                else:
                    tax_amount = Decimal("0.00")

                tax_row["tax_amount"] = tax_amount
                shipping_tax_total += tax_amount

            sale_details.append(
                {
                    "product_id": self.SHIPPING_PRODUCT_ID,
                    "measure_id": self.SHIPPING_MEASURE_ID,
                    "currency": cart.currency,
                    "quantity": Decimal("1.00"),
                    "original_price": shipping_amount,
                    "discount_factor": Decimal("0.00"),
                    "price": shipping_amount,
                    "amount": shipping_amount,
                    "subtotal": shipping_amount,
                    "discount": Decimal("0.00"),
                    "taxes": shipping_tax_total,
                    "total": shipping_amount,
                    "tax_rows": shipping_tax_rows,
                }
            )

            document_amount = self.__money(products_amount + shipping_amount)

            document_subtotal = self.__money(products_subtotal + shipping_amount)

            document_discount = self.__money(products_discount)

            document_taxes = self.__money(products_taxes + shipping_tax_total)

            document_total = self.__money(products_total + shipping_amount)

            # -------------------------------------
            # Validate PayPal capture
            # -------------------------------------

            document_currency = str(cart.currency or "mxn").lower()

            if captured_currency != document_currency:
                raise cherrypy.HTTPError(
                    409,
                    "Payment currency does not match cart",
                )

            if captured_amount != document_total:
                raise cherrypy.HTTPError(
                    409,
                    ("Payment amount does not match " "cart total: {} != {}").format(
                        captured_amount,
                        document_total,
                    ),
                )

            # -------------------------------------
            # Create sales document
            # -------------------------------------

            transaction_date = datetime.utcnow()

            document_code = ("V{serie}{branch}{date}{number}").format(
                serie=company.serie,
                branch=branch.code,
                date=Convert().datetime2str(
                    dt=None,
                    tz=timezone(branch.timezone),
                    format="%d%m%y",
                ),
                number=Serie.generate(
                    reference="sale-document",
                    key=cart.branch_id,
                    zfill=6,
                    conn=conn,
                ),
            )

            document = SaleDocument()

            document.document_id = document_id
            document.company_id = company_id
            document.branch_id = cart.branch_id
            document.warehouse_id = cart.warehouse_id
            document.seller_id = seller_id
            document.client_id = cart.client_id
            document.user_id = user_id

            document.code = document_code
            document.currency = document_currency
            document.exchange_rate = cart.exchange_rate or 1

            document.amount = float(document_amount)
            document.subtotal = float(document_subtotal)
            document.discount = float(document_discount)
            document.taxes = float(document_taxes)
            document.total = float(document_total)

            document.payment_status = "paid"
            document.payment_method = self.ECOMMERCE_PAYMENT_METHOD
            document.payment_type = self.ECOMMERCE_PAYMENT_TYPE
            document.fiscal_use = self.ECOMMERCE_FISCAL_USE

            document.transaction_date = transaction_date
            document.is_signed = False

            document.notes = ("Pedido web. PayPal order: {}").format(provider_order_id)

            document.status = "active"
            document.created_at = transaction_date
            document.updated_at = transaction_date

            document.insert(conn=conn)

            # -------------------------------------
            # Insert details and taxes
            # -------------------------------------

            for item in sale_details:

                detail = SaleDocumentProduct()

                detail.document_id = document_id
                detail.product_id = item["product_id"]
                detail.measure_id = item["measure_id"]
                detail.currency = item["currency"]

                detail.quantity = float(item["quantity"])

                detail.original_price = float(item["original_price"])

                detail.discount_factor = float(item["discount_factor"])

                detail.price = float(item["price"])
                detail.amount = float(item["amount"])
                detail.subtotal = float(item["subtotal"])
                detail.discount = float(item["discount"])
                detail.taxes = float(item["taxes"])
                detail.total = float(item["total"])

                detail.created_at = transaction_date
                detail.updated_at = transaction_date

                detail.insert(conn=conn)

                for tax_row in item["tax_rows"]:

                    document_tax = SaleDocumentTax()

                    document_tax.document_id = document_id

                    document_tax.product_id = item["product_id"]

                    document_tax.tax_id = tax_row["tax_id"]

                    document_tax.percent = float(tax_row.get("percent", 0))

                    document_tax.created_at = transaction_date

                    document_tax.updated_at = transaction_date

                    document_tax.insert(conn=conn)

            # -------------------------------------
            # Resolve postal-code IDs
            # -------------------------------------

            postal = PostalCode().where({"zip": zip_code}).one_or_none(conn=conn)

            if postal is None:
                raise cherrypy.HTTPError(
                    400,
                    "Postal code not found",
                )

            # -------------------------------------
            # Delivery address
            # -------------------------------------

            delivery = DeliveryAddress()

            delivery.document_id = document_id
            delivery.name = str(address_body["name"]).strip()

            delivery.email = str(address_body["email"]).strip()

            delivery.phone = phone

            delivery.address_street = str(address_body["street"]).strip()

            delivery.address_external_number = str(address_body["exterior_number"]).strip()

            delivery.address_internal_number = str(
                address_body.get(
                    "interior_number",
                    "",
                )
            ).strip()

            delivery.neighborhood = str(address_body["neighborhood"]).strip()

            delivery.state_id = postal.state_id
            delivery.municipality_id = postal.municipality_id

            delivery.locality_id = postal.locality_id or None

            delivery.zip = zip_code

            delivery.references = str(
                address_body.get(
                    "reference",
                    "",
                )
            ).strip()

            delivery.status = "active"
            delivery.created_at = transaction_date
            delivery.updated_at = transaction_date

            delivery.insert(conn=conn)

            # -------------------------------------
            # Payment
            # -------------------------------------

            payment_code = ("P{prefix}{date}{number}").format(
                prefix=branch.serie or "",
                date=Convert().datetime2str(
                    dt=None,
                    tz=timezone(branch.timezone),
                    format="%d%m%y",
                ),
                number=Serie.generate(
                    reference="document-payment",
                    key=cart.branch_id,
                    zfill=6,
                    conn=conn,
                ),
            )

            payment = DocumentPayment()

            payment.payment_id = str(uuid.uuid4())

            payment.document_id = document_id
            payment.branch_id = cart.branch_id
            payment.user_id = user_id

            payment.reference = document.code
            payment.code = payment_code
            payment.serie = 1

            payment.payment_method = self.ECOMMERCE_PAYMENT_METHOD

            payment.provider = provider
            payment.provider_order_id = provider_order_id

            payment.provider_transaction_id = provider_transaction_id

            payment.provider_status = provider_status
            payment.provider_data = json.dumps(
                payment_body.get("provider_data", {}),
                ensure_ascii=False,
            )

            payment.previous_balance = float(document_total)

            payment.amount = float(document_total)
            payment.pay_with = float(document_total)
            payment.change = 0.00
            payment.balance = 0.00

            payment.currency = document_currency
            payment.exchange_rate = cart.exchange_rate or 1

            payment.transaction_date = transaction_date

            payment.is_signed = False
            payment.status = "active"
            payment.created_at = transaction_date
            payment.updated_at = transaction_date

            payment.insert(conn=conn)

            # -------------------------------------
            # Convert cart
            # -------------------------------------

            cart.status = "converted"
            cart.updated_at = transaction_date
            cart.update(conn=conn)

            conn.commit(conn)

        except cherrypy.HTTPError:
            conn.rollback(conn)
            raise

        except Exception as error:
            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                "Problem creating checkout: {}".format(str(error)),
            )

        try:
            notification = Notification()

            email_products = []

            for item in sale_details:
                product = (
                    Product()
                    .where(
                        {
                            "product_id": item["product_id"],
                        }
                    )
                    .one_or_none(conn=conn)
                )

                measure = (
                    Measure()
                    .where(
                        {
                            "measure_id": item["measure_id"],
                        }
                    )
                    .one_or_none(conn=conn)
                )

                email_products.append(
                    {
                        "name": (product.short_name or product.name),
                        "measure": (measure.name if measure else ""),
                        "quantity": float(item["quantity"]),
                        "price": float(item["price"]),
                        "total": float(item["total"]),
                    }
                )

            state = (
                State()
                .where(
                    {
                        "state_id": delivery.state_id,
                    }
                )
                .one_or_none(conn=conn)
            )

            municipality = (
                Municipality()
                .where(
                    {
                        "state_id": delivery.state_id,
                    },
                    {
                        "municipality_id": delivery.municipality_id,
                    },
                )
                .one_or_none(conn=conn)
            )

            notification_data = {
                "document": {
                    **document.as_dict(),
                },
                "products": email_products,
                "delivery_address": {
                    **delivery.as_dict(),
                    "state_name": (state.name if state else ""),
                    "municipality_name": (municipality.name if municipality else ""),
                },
                "payment": {
                    **payment.as_dict(),
                },
            }

            notification.send_order_confirmation(notification_data)

            notification.send_order_notification(
                {
                    **notification_data,
                    "to": [
                        "fajadeorocs@yahoo.com.mx",
                    ],
                    "cc": [
                        "olafcazarez@gmail.com",
                    ],
                }
            )
        except Exception:
            cherrypy.log(
                "Checkout created, but notification email failed",
                traceback=True,
            )

        return {
            "document_id": document.document_id,
            "code": document.code,
            "payment_id": payment.payment_id,
            "payment_code": payment.code,
            "payment_status": document.payment_status,
            "total": float(document_total),
            "currency": document.currency,
            "already_processed": False,
        }

    # -------------------------------------------------------------------------
    # CART HELPERS
    # -------------------------------------------------------------------------

    def __get_cart_token(self):
        cart_token = cherrypy.request.headers.get("X-Cart-Token")

        if not cart_token:
            raise cherrypy.HTTPError(
                400,
                "Missing X-Cart-Token header",
            )

        return cart_token

    def __get_active_cart(self, cart_token, conn):
        return (
            ShoppingCart()
            .where(
                {"cart_token": cart_token},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

    def __validate_cart_context(
        self,
        branch_id,
        warehouse_id,
        client_id,
        conn,
    ):
        warehouse = (
            BranchOfficeWarehouse()
            .where(
                {"branch_id": branch_id},
                {"warehouse_id": warehouse_id},
            )
            .one_or_none(conn=conn)
        )

        if warehouse is None:
            raise cherrypy.HTTPError(
                400,
                "Invalid branch and warehouse combination",
            )

        client = (
            Client()
            .where(
                {"client_id": client_id},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if client is None:
            raise cherrypy.HTTPError(
                400,
                "Invalid client",
            )

    def __get_warehouse_product(
        self,
        warehouse_id,
        product_id,
        measure_id,
        conn,
    ):
        product = (
            Product()
            .where(
                _OR(
                    {"product_id": product_id},
                    {"code": product_id},
                ),
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if product is None:
            raise cherrypy.HTTPError(
                404,
                "Product not found",
            )

        product = product.as_dict()

        measure = (
            vProductMeasure()
            .where(
                {"product_id": product["product_id"]},
                {"measure_id": measure_id},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if measure is None:
            raise cherrypy.HTTPError(
                400,
                "Invalid product measure",
            )

        if hasattr(measure, "as_dict"):
            measure = measure.as_dict()

        stock = (
            Stock()
            .where(
                {"warehouse_id": warehouse_id},
                {"product_id": product["product_id"]},
                {"measure_id": measure_id},
                {"status": "active"},
            )
            .one_or_none(conn=conn)
        )

        if stock is None:
            raise cherrypy.HTTPError(
                400,
                "Product is not available in the selected warehouse",
            )

        stock_data = stock.as_dict() if hasattr(stock, "as_dict") else stock

        measure.update(
            {
                "warehouse_id": warehouse_id,
                "quantity": stock_data.get("quantity", 0),
                "price": stock_data.get("price", 0),
                "discount": stock_data.get("discount", 0),
            }
        )

        # Stock validation is intentionally disabled for the initial version.
        # It can later be enabled using measure["quantity"].

        price = self.__decimal(measure.get("price"))

        if price <= 0:
            raise cherrypy.HTTPError(
                400,
                "Product does not have a valid price",
            )

        taxes = (
            ProductTax()
            .where(
                {"product_id": product["product_id"]},
                {"status": "active"},
            )
            .all(
                conn=conn,
                collection=False,
            )
        )

        product_taxes = []

        for item in taxes:
            tax = (
                Tax()
                .where(
                    {"tax_id": item["tax_id"]},
                    {"status": "active"},
                )
                .one_or_none(conn=conn)
            )

            if tax is None:
                continue

            tax_data = tax.as_dict()
            tax_data.update(item)

            product_taxes.append(tax_data)

        return {
            "product_id": product["product_id"],
            "product": product,
            "measure": measure,
            "taxes": product_taxes,
        }

    # -------------------------------------------------------------------------
    # TAXES AND PRICING
    # -------------------------------------------------------------------------

    def __calculate_item_pricing(
        self,
        quantity,
        price,
        discount_percent,
    ):
        quantity = self.__decimal(quantity)
        original_price = self.__money(price)
        discount_percent = self.__decimal(discount_percent)

        if discount_percent < 0:
            discount_percent = Decimal("0")

        if discount_percent > 100:
            discount_percent = Decimal("100")

        discount_per_unit = original_price * discount_percent / Decimal("100")

        unit_price = self.__money(original_price - discount_per_unit)

        discount_amount = self.__money(discount_per_unit * quantity)

        return {
            "original_price": original_price,
            "unit_price": unit_price,
            "discount_amount": discount_amount,
        }

    def __save_item_taxes(
        self,
        cart_item,
        taxes,
        conn,
    ):
        sql = """
            DELETE FROM `{table}`
            WHERE `cart_item_id` = %s
        """.format(table=ShoppingCartItemTax()._TABLE)

        conn.execute(
            sql,
            cart_item.cart_item_id,
            connection=None,
            affect_data=True,
        )

        quantity = self.__decimal(cart_item.quantity)
        unit_price = self.__money(cart_item.unit_price)

        line_total = self.__money(quantity * unit_price)

        total_percent = sum(
            (self.__decimal(item.get("percent")) for item in taxes),
            Decimal("0"),
        )

        for item in taxes:
            percent = self.__decimal(item.get("percent"))

            tax_amount = Decimal("0")

            # Retail prices are tax-inclusive.
            if total_percent > 0:
                tax_amount = self.__money(line_total * percent / (Decimal("100") + total_percent))

            tax = ShoppingCartItemTax()
            tax.cart_item_id = cart_item.cart_item_id
            tax.tax_id = item["tax_id"]
            tax.percent = percent
            tax.tax_amount = tax_amount
            tax.created_at = datetime.utcnow()
            tax.updated_at = datetime.utcnow()

            tax.insert(
                ignore=True,
                conn=conn,
            )

    # -------------------------------------------------------------------------
    # SERIALIZATION
    # -------------------------------------------------------------------------

    def __serialize_cart(
        self,
        cart,
        conn,
    ):
        cart_data = cart.as_dict()

        rows = (
            ShoppingCartItem()
            .where(
                {"cart_id": cart.cart_id},
            )
            .all(
                conn=conn,
                collection=False,
            )
        )

        items = []

        subtotal = Decimal("0")
        original_subtotal = Decimal("0")
        discount_total = Decimal("0")
        tax_total = Decimal("0")
        total_quantity = Decimal("0")

        for row in rows:
            product = (
                Product()
                .where(
                    {"product_id": row["product_id"]},
                )
                .one_or_none(conn=conn)
            )

            measure = (
                Measure()
                .where(
                    {"measure_id": row["measure_id"]},
                )
                .one_or_none(conn=conn)
            )

            product_data = product.as_dict() if product is not None else {}

            measure_data = measure.as_dict() if measure is not None else {}

            quantity = self.__decimal(row.get("quantity"))

            original_price = self.__money(row.get("original_price"))

            unit_price = self.__money(row.get("unit_price"))

            discount_amount = self.__money(row.get("discount_amount"))

            original_line_total = self.__money(original_price * quantity)

            line_total = self.__money(unit_price * quantity)

            tax_rows = (
                ShoppingCartItemTax()
                .where(
                    {"cart_item_id": row["cart_item_id"]},
                )
                .all(
                    conn=conn,
                    collection=False,
                )
            )

            item_tax_total = sum(
                (self.__money(tax.get("tax_amount")) for tax in tax_rows),
                Decimal("0"),
            )

            taxes = []

            for tax_row in tax_rows:
                tax = (
                    Tax()
                    .where(
                        {"tax_id": tax_row["tax_id"]},
                    )
                    .one_or_none(conn=conn)
                )

                tax_data = tax.as_dict() if tax is not None else {}

                tax_data.update(tax_row)
                taxes.append(tax_data)

            items.append(
                {
                    **row,
                    "product": product_data,
                    "measure": measure_data,
                    "taxes": sorted(
                        taxes,
                        key=lambda item: item.get(
                            "name",
                            "",
                        ),
                    ),
                    "original_line_total": original_line_total,
                    "line_total": line_total,
                    "tax_total": item_tax_total,
                }
            )

            original_subtotal += original_line_total
            subtotal += line_total
            discount_total += discount_amount
            tax_total += item_tax_total
            total_quantity += quantity

        cart_data["items"] = sorted(
            items,
            key=lambda item: item.get(
                "product",
                {},
            ).get(
                "name",
                "",
            ),
        )

        cart_data["item_count"] = len(items)
        cart_data["total_quantity"] = total_quantity

        cart_data["totals"] = {
            "original_subtotal": self.__money(original_subtotal),
            "subtotal": self.__money(subtotal),
            "discount": self.__money(discount_total),
            "tax": self.__money(tax_total),
            "total": self.__money(subtotal),
        }

        return cart_data

    # -------------------------------------------------------------------------
    # DECIMAL HELPERS
    # -------------------------------------------------------------------------

    def __decimal(
        self,
        value,
        default="0",
    ):
        if value is None or value == "":
            value = default

        try:
            return Decimal(str(value))

        except Exception:
            return Decimal(str(default))

    def __money(self, value):
        return self.__decimal(value).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
