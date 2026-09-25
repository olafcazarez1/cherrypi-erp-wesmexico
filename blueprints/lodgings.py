import cherrypy
import pymysql

from helpers.helper_locality import HelperLocality

from utils.decorators import tools
from utils.query import _OR, Query
from utils.utils import Utils

from datetime import datetime
from models.serie import Serie

from models.lodging import Lodging
from models.lodging_amenity import LodgingAmenity
from models.lodging_amenity_assignment import LodgingAmenityAssignment
from models.lodging_reservation import LodgingReservation


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
            LodgingAmenityAssignment()
            .where(
                {"lodging_id": lodging.lodging_id},
            )
            .all(
                conn=conn,
                collection=False,
            )
        )

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
        ]
    )
    def save_lodging(self, **kwargs):

        body = cherrypy.request.json
        lodging_id = body.get("lodging_id", None)
        amenities = body.pop("amenities", [])

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
