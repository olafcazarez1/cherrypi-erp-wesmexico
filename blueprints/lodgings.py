import uuid
import json
import cherrypy
import pymysql

from helpers.helper_locality import HelperLocality

from utils.decorators import tools
from utils.query import _OR, _AND, Query
from utils.utils import Utils

from datetime import datetime, timedelta
from models.serie import Serie

from models.document import Document
from models.lodging import Lodging
from models.lodging_amenity import LodgingAmenity
from models.lodging_amenity_assignment import LodgingAmenityAssignment
from models.lodging_reservation import LodgingReservation
from models.lodging_reservation_charge import LodgingReservationCharge
from models.lodging_reservation_payment import LodgingReservationPayment

from helpers.notification import Notification


class MapLodgings(object):

    TYPES = [
        "apartment",
        "studio",
        "house",
        "room",
    ]

    STATUSES = [
        "active",
        "inactive",
    ]

    CURRENCIES = [
        "mxn",
        "usd",
    ]

    def __init__(self):
        pass

    def init(self, mapper=None):

        mapper.connect(
            "get_lodgings",
            "/catalog/lodgings",
            controller=self,
            action="get_lodgings",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_by_id",
            "/catalog/lodging/{lodging_id}",
            controller=self,
            action="get_lodging_by_id",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "save_lodging",
            "/catalog/lodging/{lodging_id}",
            controller=self,
            action="save_lodging",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "delete_lodging",
            "/catalog/lodging/{lodging_id}",
            controller=self,
            action="delete_lodging",
            conditions=dict(method=["DELETE", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_amenities",
            "/catalog/lodging/amenities",
            controller=self,
            action="get_lodging_amenities",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "search_lodgings",
            "/lodgings/search",
            controller=self,
            action="search_lodgings",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        # Reservation

        mapper.connect(
            "create_lodging_reservation",
            "/lodging-reservation",
            controller=self,
            action="create_lodging_reservation",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "patch_lodging_reservation",
            "/lodging-reservation/{reservation_id}",
            controller=self,
            action="patch_lodging_reservation",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

        mapper.connect(
            "create_manual_lodging_reservation",
            "/lodging-reservation/manual",
            controller=self,
            action="create_manual_lodging_reservation",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_reservations",
            "/lodging-reservations",
            controller=self,
            action="get_lodging_reservations",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_reservation",
            "/lodging-reservation/{reservation_id}",
            controller=self,
            action="get_lodging_reservation",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "create_lodging_reservation_payment",
            "/lodging-reservation/{reservation_id}/payment",
            controller=self,
            action="create_lodging_reservation_payment",
            conditions=dict(method=["POST", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_reservation_payments",
            "/lodging-reservation/{reservation_id}/payments",
            controller=self,
            action="get_lodging_reservation_payments",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "get_lodging_reservation_payment",
            "/lodging-reservation/{reservation_id}/payment/{payment_id}",
            controller=self,
            action="get_lodging_reservation_payment",
            conditions=dict(method=["GET", "OPTIONS"]),
        )

        mapper.connect(
            "patch_lodging_reservation_payment",
            "/lodging-reservation/{reservation_id}/payment/{payment_id}",
            controller=self,
            action="patch_lodging_reservation_payment",
            conditions=dict(method=["PATCH", "OPTIONS"]),
        )

    # -------------------------------------------------------------------------
    # LODGINGS LIST
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodgings(self, **kwargs):

        result = {
            "results": [],
            "total_rows": 0,
        }

        offset = int(kwargs.get("offset", 0))

        limit = int(kwargs.get("limit", 50))

        look_for = str(kwargs.get("look_for", "") or "").strip()

        filters = kwargs.get("filters", "[]")

        criterias = []

        if look_for:

            criterias.append(
                _OR(
                    {"code": look_for, "op": "like"},
                    {"name": look_for, "op": "like"},
                    {"description": look_for, "op": "like"},
                    {"neighborhood": look_for, "op": "like"},
                )
            )

        criterias += Utils().convert_filters(filters, force_status=True)

        query = Query(model=Lodging())

        query.where(*criterias)

        query.limit(limit)

        query.offset(offset)

        query.order_by(["+code"])

        result["results"] = query.all(collection=False)

        result["total_rows"] = query.count()

        if len(result["results"]) == 0:

            cherrypy.response.status = "204 No Content"

            return {}

        return result

    # -------------------------------------------------------------------------
    # GET LODGING
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_by_id(self, lodging_id=None, **kwargs):

        conn = Lodging().get_connection()

        lodging = (
            Lodging()
            .where(
                {"lodging_id": lodging_id},
            )
            .one_or_none(conn=conn)
        )

        if lodging is None:
            raise cherrypy.HTTPError(404, "Not Found")

        response = lodging.as_dict()

        response["amenities"] = (
            LodgingAmenity()
            .where(
                {
                    "amenity_id": (
                        LodgingAmenityAssignment()
                        .fields(["amenity_id"])
                        .where({"lodging_id": lodging.lodging_id})
                        .sql(remove_offset_limit=True)
                    ),
                    "op": "in",
                }
            )
            .all(collection=False, conn=conn)
        )

        response["photos"] = (
            Document()
            .where(
                {"parent_id": lodging.lodging_id},
            )
            .all(
                conn=conn,
                collection=False,
            )
        )

        for photo in response["photos"]:
            photo["data"] = json.loads(photo["data"])

        response.update(HelperLocality.get(item=response, conn=conn))

        return response

    # -------------------------------------------------------------------------
    # SAVE
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "lodging_id",
            "name",
            "type",
            "description",
            "bedrooms",
            "beds",
            "bathrooms",
            "max_occupancy",
            "price_per_night",
            "currency",
            "check_in_time",
            "check_out_time",
            "address_street",
            "address_external_number",
            "address_internal_number",
            "neighborhood",
            "state_id",
            "municipality_id",
            "locality_id",
            "zip",
            "observations",
            "status",
            "amenities",
            "photos",
        ]
    )
    def save_lodging(self, **kwargs):

        body = cherrypy.request.json
        lodging_id = body.get("lodging_id", None)
        amenities = body.pop("amenities", [])
        photos = body.pop("photos", [])

        conn = Lodging().get_connection()

        try:
            conn.begin(conn)

            lodging = Lodging().where({"lodging_id": lodging_id}).one_or_none(conn=conn)

            is_new = False

            if lodging is None:
                is_new = True

                body["code"] = Serie.generate(
                    reference="general",
                    key="lodging",
                    prefix="HSP-",
                    conn=conn,
                )

                lodging = Lodging()
                lodging.created_at = datetime.utcnow()

            lodging.set_attrs(body)
            lodging.updated_at = datetime.utcnow()

            lodging.insert(conn=conn) if is_new else lodging.update(conn=conn)

            # Remove amenities
            sql = ("""
                    DELETE FROM `{table}`
                    WHERE
                        `lodging_id` = %s
                """).format(
                table=LodgingAmenityAssignment()._TABLE,
            )

            args = [lodging_id]
            conn.execute(sql, *args, connection=None)

            # Insert amenities
            for amenity_id in amenities:

                assignment = LodgingAmenityAssignment()

                assignment.lodging_id = lodging_id
                assignment.amenity_id = amenity_id
                assignment.created_at = datetime.utcnow()

                assignment.insert(conn=conn)

            #
            # Remove current gallery photos
            #
            sql = ("""
                    DELETE FROM `{table}`
                    WHERE
                        `source` = %s AND
                        `parent_id` = %s AND
                        `category` = %s AND
                        `subcategory` = %s
                """).format(table=Document()._TABLE)

            conn.execute(sql, "lodging", lodging_id, "photo", "gallery", connection=None)

            #
            # Insert photos
            #
            for photo in photos:

                p_data = json.dumps(photo.pop("data", {}))

                document = Document()
                document.set_attrs(photo)

                #
                # Force lodging ownership.
                #
                document.source = "lodging"
                document.parent_id = lodging_id
                document.category = "photo"
                document.subcategory = "gallery"
                document.data = p_data

                document.status = "active"

                document.created_at = datetime.utcnow()

                document.updated_at = datetime.utcnow()

                document.insert(conn=conn)

            conn.commit(conn)

        except pymysql.err.IntegrityError as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(409, str(error))

        except Exception as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(500, str(error))

        return {}

    # -------------------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def delete_lodging(self, lodging_id=None, **kwargs):

        conn = Lodging().get_connection()

        lodging = Lodging().where({"lodging_id": lodging_id}).one_or_none(conn=conn)

        if lodging is None:

            raise cherrypy.HTTPError(404, "Not Found")

        lodging.status = "inactive"

        lodging.updated_at = datetime.utcnow()

        lodging.update(conn=conn)

        return {}

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_amenities(self, **kwargs):

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 1000)
        look_for = kwargs.get("look_for", "")
        filters = kwargs.get("filters", "[]")

        result = {
            "results": [],
            "total_rows": 0,
        }

        criterias = [
            _OR(
                {"code": look_for, "op": "like"},
                {"name": look_for, "op": "like"},
            )
        ]

        criterias = criterias + Utils().convert_filters(
            filters,
            force_status=True,
        )

        query = Query(model=LodgingAmenity())

        query.where(*criterias)
        query.limit(limit)
        query.offset(offset)
        query.order_by(["+name"])

        result["results"] = query.all(collection=False)
        result["total_rows"] = query.count()

        if len(result["results"]) == 0:
            cherrypy.response.status = "204 No Content"
            return {}

        return result

    # -------------------------------------------------------------------------
    # LODGINGS SEARCH
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    def search_lodgings(self, **kwargs):

        check_in = str(kwargs.get("check_in", "") or "").strip()

        check_out = str(kwargs.get("check_out", "") or "").strip()

        guests = int(kwargs.get("guests", 1) or 1)

        offset = int(kwargs.get("offset", 0))

        limit = int(kwargs.get("limit", 50))

        filters = kwargs.get(
            "filters",
            "[]",
        )

        # ---------------------------------------------------------------------
        # Amenities
        # ---------------------------------------------------------------------

        amenity_filter = Utils().get_filter(
            filters=filters,
            key="amenities",
        )

        amenities = amenity_filter.get("value", []) if amenity_filter else []

        if isinstance(amenities, str):

            amenity_ids = [item.strip() for item in amenities.split(",") if item.strip()]

        elif isinstance(amenities, list):

            amenity_ids = [str(item).strip() for item in amenities if str(item).strip()]

        else:

            amenity_ids = []

        # ---------------------------------------------------------------------
        # Validate dates
        # ---------------------------------------------------------------------

        if not check_in or not check_out:

            raise cherrypy.HTTPError(
                400,
                "check_in and check_out are required",
            )

        try:

            check_in_date = datetime.strptime(
                check_in,
                "%Y-%m-%d",
            ).date()

            check_out_date = datetime.strptime(
                check_out,
                "%Y-%m-%d",
            ).date()

        except ValueError:

            raise cherrypy.HTTPError(
                400,
                "Invalid date format. Expected YYYY-MM-DD",
            )

        if check_out_date <= check_in_date:

            raise cherrypy.HTTPError(
                400,
                "check_out must be greater than check_in",
            )

        if guests < 1:

            raise cherrypy.HTTPError(
                400,
                "guests must be greater than zero",
            )

        nights = (check_out_date - check_in_date).days

        # ---------------------------------------------------------------------
        # Lodging filters
        # ---------------------------------------------------------------------

        criterias = [
            {
                "max_occupancy": guests,
                "op": "gte",
            },
            {
                "lodging_id": (
                    LodgingReservation()
                    .fields(
                        [
                            "lodging_id",
                        ]
                    )
                    .where(
                        _OR(
                            {"status": "confirmed"},
                            _AND(
                                {"status": "pending_payment"},
                                {
                                    "expires_at": datetime.utcnow(),
                                    "op": "gt",
                                },
                            ),
                        ),
                        {
                            "check_in": check_out,
                            "op": "lt",
                        },
                        {
                            "check_out": check_in,
                            "op": "gt",
                        },
                    )
                    .sql(
                        remove_offset_limit=True,
                    )
                ),
                "op": "not in",
            },
        ]

        criterias = criterias + Utils().convert_filters(
            filters,
            ignore=[
                "amenities",
            ],
            force_status=True,
        )

        query = Query(
            model=Lodging(),
        )

        query.where(*criterias)

        query.limit(limit=limit)
        query.offset(offset=offset)

        query.order_by(
            [
                "+price_per_night",
                "+code",
            ]
        )

        # ---------------------------------------------------------------------
        # Load candidates
        #
        # Pagination is applied after amenities because amenities belong to
        # another table and may reduce the final result set.
        # ---------------------------------------------------------------------

        conn = Lodging().get_connection()
        lodgings = query.all(collection=False, conn=conn)
        total_rows = query.count(conn=conn)

        # ---------------------------------------------------------------------
        # Amenities filtering + response
        # ---------------------------------------------------------------------

        results = []
        for lodging in lodgings:

            lodging_id = lodging["lodging_id"]

            amenities = (
                LodgingAmenity()
                .where(
                    {
                        "amenity_id": (
                            LodgingAmenityAssignment()
                            .fields(
                                [
                                    "amenity_id",
                                ]
                            )
                            .where(
                                {
                                    "lodging_id": lodging_id,
                                },
                            )
                            .sql(remove_offset_limit=True)
                        ),
                        "op": "in",
                    }
                )
                .all(
                    collection=False,
                    conn=conn,
                )
            )

            # ---------------------------------------------------------------------
            # Amenities
            # ---------------------------------------------------------------------

            if amenity_ids:

                assigned_ids = {amenity["amenity_id"] for amenity in amenities}

                if not all(amenity_id in assigned_ids for amenity_id in amenity_ids):

                    continue

            # ---------------------------------------------------------------------
            # Result
            # ---------------------------------------------------------------------

            item = dict(lodging)

            item["nights"] = nights

            item["subtotal"] = (
                float(
                    item.get(
                        "price_per_night",
                        0,
                    )
                    or 0
                )
                * nights
            )

            item["amenities"] = amenities

            item.update(
                HelperLocality.get(
                    item=item,
                    conn=conn,
                )
            )

            results.append(item)

        # ---------------------------------------------------------------------
        # Response
        # ---------------------------------------------------------------------

        if len(results) == 0:

            cherrypy.response.status = "204 No Content"

            return {}

        return {
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "guests": guests,
            "results": results,
            "total_rows": total_rows,
        }

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "lodging_id",
            "check_in",
            "check_out",
            "guests",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
    )
    def create_lodging_reservation(self, **kwargs):

        reservation_session_id = str(
            cherrypy.request.headers.get(
                "X-Reservation-Session-Id",
                "",
            )
            or ""
        ).strip()

        if not reservation_session_id:

            raise cherrypy.HTTPError(
                400,
                "X-Reservation-Session-Id is required",
            )

        data = cherrypy.request.json

        lodging_id = data["lodging_id"]

        check_in = data["check_in"]
        check_out = data["check_out"]

        guests = int(
            data.get(
                "guests",
                1,
            )
            or 1
        )

        conn = LodgingReservation().get_connection()

        try:

            conn.begin(conn)

            # -------------------------------------------------------------
            # Lodging
            # -------------------------------------------------------------

            lodging = (
                Lodging()
                .where(
                    {
                        "lodging_id": lodging_id,
                    }
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if not lodging:

                raise cherrypy.HTTPError(
                    404,
                    "Lodging not found",
                )

            # -------------------------------------------------------------
            # Dates
            # -------------------------------------------------------------

            try:

                check_in_date = datetime.strptime(
                    check_in,
                    "%Y-%m-%d",
                ).date()

                check_out_date = datetime.strptime(
                    check_out,
                    "%Y-%m-%d",
                ).date()

            except ValueError:

                raise cherrypy.HTTPError(
                    400,
                    "Invalid date format. Expected YYYY-MM-DD",
                )

            if check_out_date <= check_in_date:

                raise cherrypy.HTTPError(
                    400,
                    "check_out must be greater than check_in",
                )

            nights = (check_out_date - check_in_date).days

            if guests < 1:

                raise cherrypy.HTTPError(
                    400,
                    "guests must be greater than zero",
                )

            if guests > int(lodging.max_occupancy or 0):

                raise cherrypy.HTTPError(
                    400,
                    "guests exceeds max occupancy",
                )

            now = datetime.utcnow()

            # -------------------------------------------------------------
            # Check confirmed reservation from any session
            # -------------------------------------------------------------

            existing = (
                LodgingReservation()
                .where(
                    {
                        "lodging_id": lodging_id,
                    },
                    {
                        "status": "confirmed",
                    },
                    {
                        "check_in": check_out,
                        "op": "lt",
                    },
                    {
                        "check_out": check_in,
                        "op": "gt",
                    },
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if existing:

                raise cherrypy.HTTPError(
                    423,
                    "Lodging is no longer available for the selected dates",
                )

            # -------------------------------------------------------------
            # Check active pending reservation from OTHER session
            # -------------------------------------------------------------

            existing = (
                LodgingReservation()
                .where(
                    {
                        "lodging_id": lodging_id,
                    },
                    {
                        "status": "pending_payment",
                    },
                    {
                        "reservation_session_id": reservation_session_id,
                        "op": "neq",
                    },
                    {
                        "expires_at": now,
                        "op": "gt",
                    },
                    {
                        "check_in": check_out,
                        "op": "lt",
                    },
                    {
                        "check_out": check_in,
                        "op": "gt",
                    },
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if existing:

                raise cherrypy.HTTPError(
                    423,
                    "Lodging is no longer available for the selected dates",
                )

            # -------------------------------------------------------------
            # Reuse reservation from CURRENT session
            # -------------------------------------------------------------

            session_reservation = (
                LodgingReservation()
                .where(
                    {
                        "reservation_session_id": reservation_session_id,
                    }
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if session_reservation:

                #
                # Defensive validation:
                # same session must belong to same stay.
                #

                if (
                    session_reservation.lodging_id != lodging_id
                    or str(session_reservation.check_in) != check_in
                    or str(session_reservation.check_out) != check_out
                ):

                    raise cherrypy.HTTPError(
                        409,
                        "Reservation session does not match the selected stay",
                    )

                #
                # Reuse even if previous hold expired,
                # because no other active reservation
                # currently owns the dates.
                #

                session_reservation.status = "pending_payment"

                session_reservation.expires_at = now + timedelta(minutes=30)

                session_reservation.updated_at = now

                session_reservation.update(
                    conn=conn,
                )

                conn.commit(conn)

                return {
                    "reservation_id": session_reservation.reservation_id,
                    "status": session_reservation.status,
                    "expires_at": session_reservation.expires_at,
                    "reused": True,
                }

            # -------------------------------------------------------------
            # Create reservation
            # -------------------------------------------------------------

            data["code"] = Serie.generate(
                reference="general",
                key="lodging_reservation",
                prefix="RSV-",
                conn=conn,
            )

            reservation_id = str(uuid.uuid4())

            reservation = LodgingReservation()

            reservation.set_attrs(
                {
                    "reservation_id": reservation_id,
                    "reservation_session_id": reservation_session_id,
                    "lodging_id": lodging_id,
                    "code": data["code"],
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": guests,
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "phone": data["phone"],
                    "status": "pending_payment",
                    "expires_at": (now + timedelta(minutes=30)),
                }
            )

            reservation.insert(
                conn=conn,
            )

            # -------------------------------------------------------------
            # Lodging charge
            # -------------------------------------------------------------

            unit_price = float(lodging.price_per_night or 0)

            subtotal = unit_price * nights

            charge = LodgingReservationCharge()

            charge.set_attrs(
                {
                    "charge_id": str(uuid.uuid4()),
                    "reservation_id": reservation_id,
                    "type": "lodging",
                    "name": "Hospedaje",
                    "description": "%s noche(s)" % nights,
                    "quantity": nights,
                    "unit_price": unit_price,
                    "subtotal": subtotal,
                    "taxes": 0,
                    "total": subtotal,
                    "currency": lodging.currency,
                }
            )

            charge.insert(
                conn=conn,
            )

            # -------------------------------------------------------------
            # Commit
            # -------------------------------------------------------------

            conn.commit(conn)

            return {
                "reservation_id": reservation_id,
                "status": "pending_payment",
                "expires_at": reservation.expires_at,
                "reused": False,
                "nights": nights,
                "charges": [
                    charge.as_dict(),
                ],
                "total": subtotal,
            }

        except pymysql.err.IntegrityError as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(
                409,
                str(error),
            )

        except cherrypy.HTTPError as error:

            conn.rollback(conn)

            raise error

        except Exception as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                str(error),
            )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_reservations(self, **kwargs):

        result = {
            "results": [],
            "total_rows": 0,
        }

        offset = int(
            kwargs.get(
                "offset",
                0,
            )
        )

        limit = int(
            kwargs.get(
                "limit",
                50,
            )
        )

        look_for = str(
            kwargs.get(
                "look_for",
                "",
            )
            or ""
        ).strip()

        start_date = str(
            kwargs.get(
                "start_date",
                "",
            )
            or ""
        ).strip()

        end_date = str(
            kwargs.get(
                "end_date",
                "",
            )
            or ""
        ).strip()

        filters = kwargs.get(
            "filters",
            "[]",
        )

        criterias = []

        # ---------------------------------------------------------------------
        # Search
        # ---------------------------------------------------------------------

        if look_for:

            criterias.append(
                _OR(
                    {
                        "code": look_for,
                        "op": "like",
                    },
                    {
                        "first_name": look_for,
                        "op": "like",
                    },
                    {
                        "last_name": look_for,
                        "op": "like",
                    },
                    {
                        "email": look_for,
                        "op": "like",
                    },
                    {
                        "phone": look_for,
                        "op": "like",
                    },
                )
            )

        # ---------------------------------------------------------------------
        # Stay date range
        #
        # Reservation overlaps requested range:
        #
        # reservation.check_in < end_date
        # reservation.check_out > start_date
        # ---------------------------------------------------------------------

        if start_date and end_date:

            criterias += [
                {
                    "check_in": end_date,
                    "op": "lt",
                },
                {
                    "check_out": start_date,
                    "op": "gt",
                },
            ]

        elif start_date:

            criterias.append(
                {
                    "check_out": start_date,
                    "op": "gte",
                }
            )

        elif end_date:

            criterias.append(
                {
                    "check_in": end_date,
                    "op": "lte",
                }
            )

        # ---------------------------------------------------------------------
        # Filters
        # ---------------------------------------------------------------------

        criterias += Utils().convert_filters(
            filters,
            force_status=False,
        )

        # ---------------------------------------------------------------------
        # Query
        # ---------------------------------------------------------------------

        query = Query(model=LodgingReservation())

        query.where(*criterias)

        query.limit(limit)

        query.offset(offset)

        query.order_by(
            [
                "-created_at",
            ]
        )

        conn = LodgingReservation().get_connection()

        reservations = query.all(
            collection=False,
            conn=conn,
        )

        result["total_rows"] = query.count(conn=conn)

        # ---------------------------------------------------------------------
        # Additional information
        # ---------------------------------------------------------------------

        for reservation in reservations:

            lodging = Lodging().where({"lodging_id": reservation["lodging_id"]}).one_or_none(conn=conn)

            reservation["lodging"] = lodging.as_dict() if lodging else None

            charges = (
                LodgingReservationCharge()
                .where({"reservation_id": reservation["reservation_id"]})
                .all(
                    collection=False,
                    conn=conn,
                    ignore_limit=True,
                )
            )

            reservation["total"] = sum(
                float(
                    charge.get(
                        "total",
                        0,
                    )
                    or 0
                )
                for charge in charges
            )

            reservation["guest_name"] = (
                "{} {}".format(
                    reservation.get(
                        "first_name",
                        "",
                    ),
                    reservation.get(
                        "last_name",
                        "",
                    ),
                )
            ).strip()

            reservation["lodging_name"] = lodging.name if lodging else ""

        result["results"] = reservations

        if not reservations:

            cherrypy.response.status = "204 No Content"

            return {}

        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_reservation(self, reservation_id, **kwargs):

        conn = LodgingReservation().get_connection()

        reservation = LodgingReservation().where({"reservation_id": reservation_id}).one_or_none(conn=conn)

        if reservation is None:

            raise cherrypy.HTTPError(404, "Reservation not found")

        charges = LodgingReservationCharge().where({"reservation_id": reservation_id}).all(collection=False, conn=conn)

        response = reservation.as_dict()

        response["lodging"] = Lodging().where({"lodging_id": reservation.lodging_id}).one_or_none(conn=conn).as_dict()
        response["charges"] = charges

        return response

    # -------------------------------------------------------------------------
    # CREATE RESERVATION PAYMENT
    # -------------------------------------------------------------------------

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "provider",
        ]
    )
    def create_lodging_reservation_payment(self, reservation_id, **kwargs):

        body = cherrypy.request.json

        provider = body.get("provider", "")

        if provider not in [
            "paypal",
            "mercado_pago",
        ]:

            raise cherrypy.HTTPError(
                400,
                "Invalid payment provider",
            )

        conn = LodgingReservation().get_connection()
        try:

            #
            # Reservation
            #

            reservation = (
                LodgingReservation()
                .where(
                    {
                        "reservation_id": reservation_id,
                    }
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if not reservation:

                raise cherrypy.HTTPError(
                    404,
                    "Reservation not found",
                )

            #
            # Only pending reservations can
            # create new payment attempts.
            #

            if reservation.status != "pending_payment":

                raise cherrypy.HTTPError(
                    409,
                    "Reservation is not pending payment",
                )

            #
            # Validate expiration.
            #

            now = datetime.utcnow()

            if reservation.expires_at and reservation.expires_at <= now:

                raise cherrypy.HTTPError(
                    409,
                    "Reservation has expired",
                )

            #
            # Check if reservation was already paid.
            #

            paid_payment = (
                LodgingReservationPayment()
                .where(
                    {
                        "reservation_id": reservation_id,
                    },
                    {
                        "status": "paid",
                    },
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if paid_payment:

                raise cherrypy.HTTPError(
                    409,
                    "Reservation is already paid",
                )

            #
            # Calculate amount from persisted charges.
            #
            # Never trust an amount coming from
            # the browser.
            #

            charges = (
                LodgingReservationCharge()
                .where(
                    {
                        "reservation_id": reservation_id,
                    }
                )
                .all(
                    collection=False,
                    conn=conn,
                    ignore_limit=True,
                )
            )

            amount = sum(float(charge.get("total", 0) or 0) for charge in charges)

            if amount <= 0:

                raise cherrypy.HTTPError(
                    409,
                    "Reservation has no payable charges",
                )

            #
            # Create payment attempt.
            #

            payment = LodgingReservationPayment()

            payment.payment_id = str(uuid.uuid4())
            payment.reservation_id = reservation_id
            payment.provider = provider
            payment.provider_reference = ""
            payment.provider_payment_id = ""
            payment.amount = amount
            payment.currency = reservation.currency
            payment.status = "pending"
            payment.created_at = datetime.utcnow()
            payment.updated_at = datetime.utcnow()

            payment.insert(
                conn=conn,
            )
            return payment.as_dict()

        except pymysql.err.IntegrityError as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(409, str(error))

        except cherrypy.HTTPError as error:

            conn.rollback(conn)

            raise error

        except Exception as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(500, str(error))

        finally:
            pass

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "status",
        ]
    )
    def patch_lodging_reservation(self, reservation_id, **kwargs):

        body = cherrypy.request.json

        allowed = [
            "status",
        ]

        for key in list(body.keys()):
            if key not in allowed:
                body.pop(key)

        conn = LodgingReservation().get_connection()

        reservation = (
            LodgingReservation()
            .where(
                {
                    "reservation_id": reservation_id,
                }
            )
            .one_or_none(
                conn=conn,
            )
        )

        if not reservation:

            raise cherrypy.HTTPError(
                404,
                "Reservation not found",
            )

        reservation.set_attrs(body)
        reservation.updated_at = datetime.utcnow()

        reservation.update(conn=conn)

        return reservation.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    @tools.validate_body_params(
        [
            "lodging_id",
            "check_in",
            "check_out",
            "adults",
            "children",
            "first_name",
            "last_name",
            "payment_type",
        ]
    )
    def create_manual_lodging_reservation(self, **kwargs):

        data = cherrypy.request.json

        lodging_id = data.get("lodging_id")

        payment_type = data.get(
            "payment_type",
            "",
        )

        if payment_type not in [
            "transfer",
            "courtesy",
        ]:

            raise cherrypy.HTTPError(
                400,
                "Invalid payment type",
            )

        try:

            check_in = datetime.strptime(
                data.get("check_in"),
                "%Y-%m-%d",
            )

            check_out = datetime.strptime(
                data.get("check_out"),
                "%Y-%m-%d",
            )

        except Exception:

            raise cherrypy.HTTPError(
                400,
                "Invalid reservation dates",
            )

        if check_out <= check_in:

            raise cherrypy.HTTPError(
                400,
                "check_out must be after check_in",
            )

        adults = int(
            data.get(
                "adults",
                0,
            )
            or 0
        )

        children = int(
            data.get(
                "children",
                0,
            )
            or 0
        )

        guests = adults + children

        if adults < 1:

            raise cherrypy.HTTPError(
                400,
                "At least one adult is required",
            )

        nights = (check_out - check_in).days

        conn = LodgingReservation().get_connection()

        try:

            # -------------------------------------------------------------
            # Lodging
            # -------------------------------------------------------------

            lodging = (
                Lodging()
                .where(
                    {
                        "lodging_id": lodging_id,
                    },
                    {
                        "status": "active",
                    },
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if not lodging:

                raise cherrypy.HTTPError(
                    404,
                    "Lodging not found",
                )

            if guests > int(lodging.max_occupancy or 0):

                raise cherrypy.HTTPError(
                    400,
                    "guests exceeds max occupancy",
                )

            # -------------------------------------------------------------
            # Availability
            #
            # We MUST check again here.
            # The availability search in the modal is not enough because
            # another reservation may have been created afterwards.
            # -------------------------------------------------------------

            existing = (
                LodgingReservation()
                .where(
                    {
                        "lodging_id": lodging_id,
                    },
                    {
                        "status": "confirmed",
                    },
                    {
                        "check_in": check_out,
                        "op": "lt",
                    },
                    {
                        "check_out": check_in,
                        "op": "gt",
                    },
                )
                .one_or_none(
                    conn=conn,
                )
            )

            if existing is None:

                existing = (
                    LodgingReservation()
                    .where(
                        {
                            "lodging_id": lodging_id,
                        },
                        {
                            "status": "pending_payment",
                        },
                        {
                            "expires_at": datetime.utcnow(),
                            "op": "gt",
                        },
                        {
                            "check_in": check_out,
                            "op": "lt",
                        },
                        {
                            "check_out": check_in,
                            "op": "gt",
                        },
                    )
                    .one_or_none(
                        conn=conn,
                    )
                )

            if existing:

                raise cherrypy.HTTPError(
                    409,
                    "Lodging is not available for the selected dates",
                )

            # -------------------------------------------------------------
            # Reservation
            # -------------------------------------------------------------

            code = Serie.generate(
                reference="general",
                key="lodging_reservation",
                prefix="RSV-",
                conn=conn,
            )

            reservation_id = str(uuid.uuid4())

            reservation = LodgingReservation()

            reservation.set_attrs(
                {
                    "reservation_id": reservation_id,
                    "lodging_id": lodging_id,
                    "code": code,
                    "check_in": check_in,
                    "check_out": check_out,
                    "adults": adults,
                    "children": children,
                    "guests": guests,
                    "nights": nights,
                    "first_name": data.get(
                        "first_name",
                        "",
                    ),
                    "last_name": data.get(
                        "last_name",
                        "",
                    ),
                    "email": data.get(
                        "email",
                        "",
                    ),
                    "phone": data.get(
                        "phone",
                        "",
                    ),
                    "currency": lodging.currency,
                    "observations": data.get(
                        "observations",
                        "",
                    ),
                    "status": "confirmed",
                    "expires_at": None,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            )

            reservation.insert(
                conn=conn,
            )

            # -------------------------------------------------------------
            # Charge
            # -------------------------------------------------------------

            unit_price = float(lodging.price_per_night or 0)

            if payment_type == "courtesy":

                unit_price = 0

            subtotal = unit_price * nights

            charge = LodgingReservationCharge()

            charge.set_attrs(
                {
                    "charge_id": str(uuid.uuid4()),
                    "reservation_id": reservation_id,
                    "type": "lodging",
                    "name": ("Hospedaje / Cortesía" if payment_type == "courtesy" else "Hospedaje"),
                    "description": "%s noche(s)" % nights,
                    "quantity": nights,
                    "unit_price": unit_price,
                    "subtotal": subtotal,
                    "taxes": 0,
                    "total": subtotal,
                    "currency": lodging.currency,
                    "status": "active",
                }
            )

            charge.insert(
                conn=conn,
            )

            # -------------------------------------------------------------
            # Payment
            # -------------------------------------------------------------

            payment = LodgingReservationPayment()

            payment.set_attrs(
                {
                    "payment_id": str(uuid.uuid4()),
                    "reservation_id": reservation_id,
                    "provider": payment_type,
                    "provider_reference": "",
                    "provider_payment_id": "",
                    "amount": subtotal,
                    "currency": lodging.currency,
                    "status": "paid",
                }
            )

            payment.insert(
                conn=conn,
            )

            # -------------------------------------------------------------
            # Commit
            # -------------------------------------------------------------

            conn.commit(conn)

            return {
                "reservation_id": reservation_id,
                "code": code,
                "status": "confirmed",
                "payment_type": payment_type,
                "nights": nights,
                "total": subtotal,
                "charge": charge.as_dict(),
                "payment": payment.as_dict(),
            }

        except pymysql.err.IntegrityError as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(
                409,
                str(error),
            )

        except cherrypy.HTTPError as error:

            conn.rollback(conn)

            raise error

        except Exception as error:

            conn.rollback(conn)

            raise cherrypy.HTTPError(
                500,
                str(error),
            )

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_reservation_payments(self, reservation_id, **kwargs):

        result = {
            "results": [],
            "total_rows": 0,
        }

        conn = LodgingReservation().get_connection()
        reservation = (
            LodgingReservation()
            .where(
                {
                    "reservation_id": reservation_id,
                }
            )
            .one_or_none(
                conn=conn,
            )
        )

        if not reservation:

            raise cherrypy.HTTPError(
                404,
                "Reservation not found",
            )

        payments = (
            LodgingReservationPayment()
            .where(
                {
                    "reservation_id": reservation_id,
                }
            )
            .all(
                collection=False,
                conn=conn,
                ignore_limit=True,
            )
        )

        result["results"] = payments
        result["total_rows"] = len(payments)
        return result

    @tools.cors
    @cherrypy.tools.json_out()
    @tools.secured()
    def get_lodging_reservation_payment(self, reservation_id, payment_id, **kwargs):

        conn = LodgingReservationPayment().get_connection()

        payment = (
            LodgingReservationPayment()
            .where(
                {
                    "reservation_id": reservation_id,
                    "payment_id": payment_id,
                }
            )
            .one_or_none(
                conn=conn,
            )
        )

        if not payment:

            raise cherrypy.HTTPError(
                404,
                "Payment not found",
            )

        return payment.as_dict()

    # @tools.cors
    # @cherrypy.tools.json_out()
    # @cherrypy.tools.json_in()
    # @tools.secured()
    # def patch_lodging_reservation_payment(self, reservation_id, payment_id, **kwargs):
    #     allowed = [
    #         "provider_reference",
    #         "provider_payment_id",
    #         "status",
    #     ]

    #     body = cherrypy.request.json

    #     conn = LodgingReservationPayment().get_connection()

    #     payment = (
    #         LodgingReservationPayment()
    #         .where(
    #             {
    #                 "reservation_id": reservation_id,
    #                 "payment_id": payment_id,
    #             }
    #         )
    #         .one_or_none(
    #             conn=conn,
    #         )
    #     )

    #     if not payment:

    #         raise cherrypy.HTTPError(
    #             404,
    #             "Payment not found",
    #         )

    #     for key in list(body.keys()):
    #         if key not in allowed:
    #             body.pop(key)

    #     payment.set_attrs(body)
    #     payment.updated_at = datetime.utcnow()

    #     payment.update(conn=conn)

    #     return payment.as_dict()

    @tools.cors
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @tools.secured()
    def patch_lodging_reservation_payment(self, reservation_id, payment_id, **kwargs):
        allowed = [
            "provider_reference",
            "provider_payment_id",
            "status",
        ]

        body = cherrypy.request.json

        conn = LodgingReservationPayment().get_connection()

        payment = (
            LodgingReservationPayment()
            .where(
                {
                    "reservation_id": reservation_id,
                    "payment_id": payment_id,
                }
            )
            .one_or_none(
                conn=conn,
            )
        )

        if not payment:

            raise cherrypy.HTTPError(
                404,
                "Payment not found",
            )

        previous_status = payment.status

        for key in list(body.keys()):

            if key not in allowed:

                body.pop(key)

        payment.set_attrs(body)

        payment.updated_at = datetime.utcnow()

        payment.update(
            conn=conn,
        )

        #
        # Reservation confirmation notification
        #
        # Only send when the payment changes
        # from a non-paid state to paid.
        #

        became_paid = previous_status != "paid" and payment.status == "paid"

        if became_paid:

            try:

                reservation = self.get_lodging_reservation(reservation_id)
                charges = reservation.get("charges", [])
                lodging = reservation.get("lodging", {})

                total = sum(
                    float(
                        charge.get(
                            "total",
                            0,
                        )
                        or 0
                    )
                    for charge in charges
                )

                notification_data = {
                    "reservation": reservation.as_dict(),
                    "lodging": lodging.as_dict(),
                    "payment": payment.as_dict(),
                    "charges": charges,
                    "total": total,
                }

                notification = Notification()

                notification.send_lodging_reservation_confirmation(notification_data)

            except Exception as error:

                #
                # Important:
                #
                # Payment was already confirmed.
                # An email failure must NOT turn
                # the payment request into a failure.
                #

                print(
                    "Lodging reservation confirmation " "email failed:",
                    error,
                )

        return payment.as_dict()
