import uuid

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

import cherrypy

from utils.decorators import tools
from utils.query import _OR

from models.branch_office_warehouse import BranchOfficeWarehouse
from models.shopping_cart import ShoppingCart
from models.shopping_cart_item import ShoppingCartItem
from models.shopping_cart_item_tax import ShoppingCartItemTax

from models.warehouse import Warehouse
from models.client import Client
from models.product import Product
from models.category import Category
from models.subcategory import SubCategory
from models.measure import Measure
from models.stock import Stock
from models.product_tax import ProductTax
from models.tax import Tax
from views.product_measure import vProductMeasure


class MapShoppingCart(object):

    DEFAULT_CURRENCY = "mxn"
    DEFAULT_EXCHANGE_RATE = Decimal("1")
    CART_EXPIRATION_DAYS = 30

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

        currency = str(
            body.get("currency", self.DEFAULT_CURRENCY)
        ).lower()

        exchange_rate = self.__decimal(
            body.get("exchange_rate", self.DEFAULT_EXCHANGE_RATE)
        )

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
            cart.expires_at = (
                now + timedelta(days=self.CART_EXPIRATION_DAYS)
            )

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

            new_quantity = (
                self.__decimal(item.quantity)
                + quantity
            )

            measure = warehouse_product["measure"]

            pricing = self.__calculate_item_pricing(
                quantity=new_quantity,
                price=measure["price"],
                discount_percent=measure["discount"],
            )

            item.equivalence = self.__decimal(
                measure.get("equivalence", 1)
            )

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
    def shopping_cart_update_item(
        self,
        cart_item_id=None,
        **kwargs
    ):

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

                item.equivalence = self.__decimal(
                    measure.get("equivalence", 1)
                )

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
    def shopping_cart_delete_item(
        self,
        cart_item_id=None,
        **kwargs
    ):

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

        stock_data = (
            stock.as_dict()
            if hasattr(stock, "as_dict")
            else stock
        )

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

        discount_per_unit = (
            original_price
            * discount_percent
            / Decimal("100")
        )

        unit_price = self.__money(
            original_price - discount_per_unit
        )

        discount_amount = self.__money(
            discount_per_unit * quantity
        )

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
        """.format(
            table=ShoppingCartItemTax()._TABLE
        )

        conn.execute(
            sql,
            cart_item.cart_item_id,
            connection=None,
            affect_data=True,
        )

        quantity = self.__decimal(cart_item.quantity)
        unit_price = self.__money(cart_item.unit_price)

        line_total = self.__money(
            quantity * unit_price
        )

        total_percent = sum(
            (
                self.__decimal(item.get("percent"))
                for item in taxes
            ),
            Decimal("0"),
        )

        for item in taxes:
            percent = self.__decimal(
                item.get("percent")
            )

            tax_amount = Decimal("0")

            # Retail prices are tax-inclusive.
            if total_percent > 0:
                tax_amount = self.__money(
                    line_total
                    * percent
                    / (
                        Decimal("100")
                        + total_percent
                    )
                )

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

            product_data = (
                product.as_dict()
                if product is not None
                else {}
            )

            measure_data = (
                measure.as_dict()
                if measure is not None
                else {}
            )

            quantity = self.__decimal(
                row.get("quantity")
            )

            original_price = self.__money(
                row.get("original_price")
            )

            unit_price = self.__money(
                row.get("unit_price")
            )

            discount_amount = self.__money(
                row.get("discount_amount")
            )

            original_line_total = self.__money(
                original_price * quantity
            )

            line_total = self.__money(
                unit_price * quantity
            )

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
                (
                    self.__money(
                        tax.get("tax_amount")
                    )
                    for tax in tax_rows
                ),
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

                tax_data = (
                    tax.as_dict()
                    if tax is not None
                    else {}
                )

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
            "original_subtotal": self.__money(
                original_subtotal
            ),
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